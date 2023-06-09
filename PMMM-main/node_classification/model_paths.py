import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class Op(nn.Module):

    def __init__(self):
        super(Op, self).__init__()
    
    def forward(self, x, adjs, idxes):
        ratio = 1/len(idxes)
        return sum(ratio * torch.spmm(adjs[idx], x) for idx in idxes)


class Op_sum(nn.Module):
    def __init__(self):
        super(Op_sum, self).__init__()

    def forward(self, x, adjs, idxes):
        res = 0
        ratio = 1/len(idxes)
        for idx in idxes:
            i = adjs[idx]._indices()
            value = adjs[idx]._values()
            value = torch.ones(value.size()).cuda()
            s = torch.sparse_coo_tensor(i, value, adjs[idx].size())
            res += ratio * torch.spmm(s, x)
        return res



class Cell(nn.Module):

    def __init__(self, n_step, n_hid_prev, n_hid, use_norm = True, use_nl = True, ratio = 1):
        super(Cell, self).__init__()
        
        self.affine = nn.Linear(n_hid_prev, n_hid)
        self.n_step = n_step
        self.norm = nn.LayerNorm(n_hid) if use_norm is True else lambda x : x
        self.use_nl = use_nl          
        self.ops_seq = nn.ModuleList()
        self.ops_res = nn.ModuleList()
        self.ratio = ratio
        op = Op()

        for i in range(self.n_step):
            self.ops_seq.append(op)
        for i in range(1, self.n_step):
            for j in range(i):
                self.ops_res.append(op)
    
    def forward(self, x, adjs, idxes_seq, idxes_res):
        
        x = self.affine(x)
        states = [x]
        offset = 0
        for i in range(self.n_step):
            seqi = self.ops_seq[i](states[i], adjs[:-1], idxes_seq[i]) #! exclude zero Op
            resi = sum(self.ops_res[offset + j](h, adjs, idxes_res[offset + j]) for j, h in enumerate(states[:i]))
            offset += i
            states.append(seqi + self.ratio * resi) 

        output = self.norm(states[-1])
        if self.use_nl:
            output = F.gelu(output)
        return output


class Model_paths(nn.Module):

    def __init__(self, in_dim, n_hid, num_node_types, n_classes, n_steps, ratio, dropout = None, attn_dim = 64, use_norm = True, out_nl = True, in_nl = False):
        super(Model_paths, self).__init__()
        self.num_node_types = num_node_types
        self.in_nl = in_nl
        self.n_hid = n_hid
        self.ws = nn.ModuleList()
        for i in range(num_node_types):
            self.ws.append(nn.Linear(in_dim, n_hid))
        assert(isinstance(n_steps, list))
        self.metas = nn.ModuleList()
        for i in range(len(n_steps)):
            self.metas.append(Cell(n_steps[i], n_hid, n_hid, use_norm = use_norm, use_nl = out_nl, ratio = ratio))
        
        #* [Optional] Combine more than one meta graph?
        self.attn_fc1 = nn.Linear(n_hid, attn_dim)
        self.attn_fc2 = nn.Linear(attn_dim, 1)

        #* node classification
        self.classifier = nn.Linear(n_hid, n_classes)
        self.feats_drop = nn.Dropout(dropout) if dropout is not None else lambda x : x 
    
    def forward(self, node_feats, node_types, adjs, idxes_seq, idxes_res):
        hid = torch.zeros((node_types.size(0), self.n_hid)).cuda()
        for i in range(self.num_node_types):
            idx = (node_types == i)
            hid[idx] = self.ws[i](node_feats[idx])
        if self.in_nl:
            hid = torch.tanh(hid)
        hid = self.feats_drop(hid)
        temps = []; attns = []
        for i, meta in enumerate(self.metas):
            hidi = meta(hid, adjs, idxes_seq[i], idxes_res[i])
            temps.append(hidi)
            attni = self.attn_fc2(torch.tanh(self.attn_fc1(temps[-1])))
            attns.append(attni)
        
        hids = torch.stack(temps, dim=0).transpose(0, 1)
        attns = F.softmax(torch.cat(attns, dim=-1), dim=-1)
        out = (attns.unsqueeze(dim=-1) * hids).sum(dim=1)
        logits = self.classifier(out)

        return logits
