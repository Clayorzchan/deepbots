from supervisor_abstract import AbstractSupervisor
from abc import abstractmethod


class SupervisorEmitterReceiver(AbstractSupervisor):
    def __init__(self, time_step=None):
        super(SupervisorEmitterReceiver, self).__init__(time_step)

    def initialize_coms(self,
                        emitter_name='emitter',
                        receiver_name='receiver'):

        self.emitter = self.supervisor.getEmitter(emitter_name)
        self.receiver = self.supervisor.getReceiver(receiver_name)

        self.receiver.enable(self.timestep)
        return self.emitter, self.receiver

    def do_action(self, action):
        self.handle_emitter(action)

    @abstractmethod
    def handle_emitter(self, action):
        pass

    @abstractmethod
    def handle_receiver(self):
        pass


class SupervisorCSV(SupervisorEmitterReceiver):
    def __init__(self, time_step=None,
                 emitter_name='emitter',
                 receiver_name='receiver'):
        super(SupervisorCSV, self).__init__(time_step)
        super().initialize_coms(emitter_name, receiver_name)

        self._last_mesage = None

    def handle_emitter(self, action):
        message = (','.join(action)).encode('utf-8')
        self.emitter.send(message)

    def handle_receiver(self):
        if self.receiver.getQueueLength() > 0:
            string_message = self.receiver.getData().decode('utf-8')
            self._last_mesage = string_message.split(',')

            self.receiver.nextPacket()
        return self._last_mesage
