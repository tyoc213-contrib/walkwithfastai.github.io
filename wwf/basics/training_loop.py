# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/06_basics.training_loop.ipynb (unless otherwise specified).

__all__ = []

# Internal Cell
from fastcore.xtras import dict2obj

_event2doc = {
    'after_create': "Called after the `Learner` is created",
    'before_fit': "Called before starting training or inference, ideal for initial setup",
    'before_epoch': "Called at the beginning of each epoch, useful for any behavior you need to reset at each epoch",
    'before_train': "Called at the beginning of the training part of an epoch",
    'before_batch': "Called at the beginning of each batch, just after drawing said batch.\nIt can be used to do any setup necessary for the batch or to change the input/target before it goes in the model",
    'after_pred': "Called after computing the output of the model on the batch. It can be used to change that output before it's fed to the loss",
    'after_loss': "Called after the loss has been computed, but before the backward pass. It can be used to add any penalty to the loss",
    'before_backward': "Called after the loss has been computed, but only in training mode (i.e. when the backward pass will be used)",
    'before_step': "Called after the backward pass, but before the update of the parameters. It can be used to do any change to the gradients before said update",
    'after_step': "Called after the step and before the gradients are zeroed",
    'after_batch': "Called at the end of a batch, for any clean-up before the next one",
    'after_train': "Called at the end of the training phase of an epoch",
    'before_validate': "Called at the beginning of the validation phase of an epoch, useful for any setup needed specifically for validation",
    'after_validate': "Called at the end of the validation part of an epoch",
    'after_epoch': "Called at the end of an epoch, for any clean-up before the next one",
    'after_fit': "Called at the end of training, for final clean-up",
    'after_cancel_batch': "Reached immediately after a CancelBatchException before proceeding to after_batch",
    'after_cancel_train': "Reached immediately after a CancelTrainException before proceeding to after_epoch",
    'after_cancel_validate': "Reached immediately after a CancelValidException before proceeding to after_epoch",
    'after_cancel_epoch': "Reached immediately after a CancelEpochException before proceeding to after_epoch",
    'after_cancel_fit': "Reached immediately after a CancelFitException before proceeding to after_fit"
}

event2doc = dict2obj(_event2doc)

# Cell
from typing import Union, List

from fastai.callback.core import Callback
from fastcore.dispatch import patch
from fastcore.xtras import is_listy, listify
from fastai.learner import _loop, Learner #list of all fastai events


# Cell
def _print_cb(cb:Callback, event:str, indent:int=0):
    "Prints what `cb` does during `event` with potential `indent`"
    if getattr(cb, event).__doc__ is not None:
        print(f'{" "*(indent+4)} - {cb}: \n{" "*(indent+8)} - {getattr(cb, event).__doc__}')
    else:
        print(f'{" "*(indent+4)} - {cb})

# Cell
@patch
def show_training_loop(self:Learner, verbose:bool=False, cbs:Union[None,list,Callback]=None):
    "Show each step in the training loop, potentially with Callback event descriptions"
    if cbs is not None: self.add_cbs(cbs) if is_listy(cbs) else self.add_cbs(listify(cbs))
    indent = 0
    for s in _loop:
        if s.startswith('Start'): print(f'{" "*indent}{s}'); indent += 3
        elif s.startswith('End'): indent -= 3; print(f'{" "*indent}{s}')
        else:
            if not verbose:
                print(f'{" "*indent} - {s}:', self.ordered_cbs(s))
            else:
                print(f'{" "*indent} - {s}:')
                for cb in self.ordered_cbs(s):
                    _print_cb(cb, s, indent)
    if cbs is not None: self.remove_cbs(cbs) if is_listy(cbs) else self.remove_cbs(listify(cbs))