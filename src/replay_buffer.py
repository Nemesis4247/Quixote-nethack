import torch
from collections import deque, namedtuple
import random
import numpy as np
from utils import calculate_input_tensor
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu")


class ReplayBuffer:
    """Fixed-size buffer to store experience tuples."""

    def __init__(self, action_size, buffer_size, batch_size, seed):
        """Initialize a ReplayBuffer object.
        Params
        ======
            action_size (int): dimension of each action
            buffer_size (int): maximum size of buffer
            batch_size (int): size of each training batch
            seed (int): random seed
        """
        self.action_size = action_size
        self.memory = deque(maxlen=buffer_size)
        self.batch_size = batch_size
        self.experience = namedtuple("Experience", field_names=[
                                     "state", "action", "reward", "next_state", "done"])
        self.seed = random.seed(seed)

    def add(self, state, action, reward, next_state, done):
        """Add a new experience to memory."""
        e = self.experience(state, action, reward, next_state, done)
        self.memory.append(e)

    def sample(self):
        """Randomly sample a batch of experiences from memory."""
        experiences = random.sample(self.memory, k=self.batch_size)

        # states = torch.from_numpy(
        #     np.vstack([e.state for e in experiences if e is not None])).float().to(device)
        # actions = torch.from_numpy(
        #     np.vstack([e.action for e in experiences if e is not None])).long().to(device)
        # rewards = torch.from_numpy(
        #     np.vstack([e.reward for e in experiences if e is not None])).float().to(device)
        # next_states = torch.from_numpy(np.vstack(
        #     [e.next_state for e in experiences if e is not None])).float().to(device)
        # dones = torch.from_numpy(np.vstack(
        #     [e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(device)

        states = torch.stack([calculate_input_tensor(e.state, device) for e in experiences])
        # actions = torch.stack([torch.Tensor([e.action]) for e in experiences])
        actions = [e.action for e in experiences]
        rewards = torch.stack([torch.Tensor([e.reward]) for e in experiences])
        next_states = torch.stack([calculate_input_tensor(e.next_state, device) for e in experiences])
        dones = torch.stack([torch.Tensor([e.done]) for e in experiences])

        return (states, actions, rewards, next_states, dones)

    def __len__(self):
        """Return the current size of internal memory."""
        return len(self.memory)
