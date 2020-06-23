import numpy as np
import torch
from torch.optim.optimizer import Optimizer


class BitSampler(object):
    def __init__(self, cuda=False):
        self.cuda = cuda
        self.dtype = torch.cuda.bool if cuda else torch.bool

    def sample(self, x):
        """Returns a zero-grid with a random entry flipped"""
        size = x.size()
        result = torch.zeros(size, dtype=self.dtype)
        index = tuple([torch.randint(0, s, (1,)).item() for s in size])
        result[index] = True
        return x.logical_xor_(result)


class SimulatedAnnealing(Optimizer):
    def __init__(self, params, sampler, lr=1.):
        defaults = dict(sampler=sampler, lr=lr)
        super().__init__(params, defaults)

    def step(self, closure=None):
        """
        Compare the current state to a randomized state and switch if the
        energy is lower or the metropolis criterion is satisfied.
        """
        if closure is None:
            raise Exception("loss closure is required to do SA")

        loss = closure()

        for group in self.param_groups:
            sampler = group['sampler']

            # clone parameters to revert back to the old state if needed
            cloned_params = [p.clone() for p in group['params']]

            for p in group['params']:
                p.data = group['sampler'].sample(p.data)

            # re-evaluate the loss function with the randomly flipped bit
            loss_perturbed = closure()
            final_loss, is_swapped = self.anneal(loss, loss_perturbed, group['lr'])
            
            # swap back to the cloned parameters
            if not is_swapped:
                for p, pbkp in zip(group['params'], cloned_params):
                    p.data = pbkp.data

            return final_loss

    def anneal(self, loss, loss_perturbed, tau):
        """Return the new loss """
        def acceptance_prob(old, new, temp):
            return torch.exp((old - new)/temp)

        if loss_perturbed.item() < loss.item():
            return loss_perturbed, True
        else:
            # evaluate the metropolis criterion
            ap = acceptance_prob(loss, loss_perturbed, tau)
            if ap.item() > np.random.rand():
                return loss_perturbed, True
            return loss, False