from Infrastructure.HookLibrary.Hook_Collection import Hook_Collection
from Infrastructure.PacketLibrary.Packet_Bus import forward_packet, drop_packet, add_to_intercept

class Hook_Collection_Manager:

    def __init__(self):
        self.hook_collection = []
        self.n_hook_collections = 0

    def execute_hooks(self, packet):
        order = ""
        for i in range(0, self.n_hook_collections):
            if not self.hook_collection[i].enabled:
                continue
            for j in range(0, self.hook_collection[i].n_hooks):
                order = self.hook_collection[i].hook[j].execute_hook(packet)
                if order == "Forward":
                    forward_packet("hook", packet)
                    return
                elif order == "Drop":
                    drop_packet("hook", packet)
                    return

    def add_hook_collection(self, hook_collection):
        if hook_collection.sequence_number >= self.n_hook_collections or hook_collection.sequence_number < 0:
            hook_collection.sequence_number = self.n_hook_collections
            self.hook_collection.append(hook_collection)
        else:
            self.hook_collection.append(Hook_Collection())
            for i in reversed(hook_collection.sequence_number, self.n_hook_collections):
                self.hook_collection[i+1] = self.hook_collection[i]
                self.hook_collection[i+1].sequence_number += 1
            self.hook_collection[hook_collection.sequence_number] = hook_collection
        self.n_hook_collections += 1

    def remove_hook_collection(self, hook_collection):
        if hook_collection.sequence_number > self.n_hook_collections or hook_collection.sequence_number < 0:
            return
        sn = hook_collection.sequence_number
        del self.hook_collection[sn]
        for i in range(sn, self.n_hook_collections):
            self.hook_collection[i].sequence_number -= 1
        self.n_hook_collections -= 1
