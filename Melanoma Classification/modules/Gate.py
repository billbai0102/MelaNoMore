import torch
import torch.nn as nn

class Gate(nn.Module):
    def __init__(self, operators, analyst, output_dims=[1]):
        super(Gate, self).__init__()
        self.operators = nn.ModuleList(operators)
        self.analyst = analyst
        self.op_length = len(operators)
        self.output_dims = output_dims

    def forward(self, inputs, context):
        pred = torch.softmax(self.analyst(context), dim=-1)
        stacked_ops = torch.stack([op(inputs) for op in self.operators], dim=1)
        pred_per_op = torch.reshape(pred, [-1, self.op_length, *self.output_dims])
        mult_ops = pred_per_op * stacked_ops
        op = torch.sum(mult_ops, dim=1)
        return op