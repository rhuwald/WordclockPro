from machine import Pin
from micropython import schedule
from time import ticks_ms

class PinMixin:

    @property
    def pin(self):
        return self._pin_num

    def __str__(self):
        return "{} (pin {})".format(self.__class__.__name__, self._pin_num)

class PinsMixin:

    @property
    def pins(self):
        return self._pin_nums

    def __str__(self):
        return "{} (pins - {})".format(self.__class__.__name__, self._pin_nums)
  

class InputDevice:
    def __init__(self, active_state=None):
        self._active_state = active_state

    @property
    def active_state(self):
        return self._active_state

    @active_state.setter
    def active_state(self, value):
        self._active_state = True if value else False
        self._inactive_state = False if value else True
        
    @property
    def value(self):
        return self._read()

class DigitalInputDevice(InputDevice, PinMixin):
    def __init__(self, pin, pull_up=False, active_state=None, bounce_time=None):
        super().__init__(active_state)
        self._pin_num = pin
        self._pin = Pin(
            pin,
            mode=Pin.IN,
            pull=Pin.PULL_UP if pull_up else Pin.PULL_DOWN)
        self._bounce_time = bounce_time
        
        if active_state is None:
            self._active_state = False if pull_up else True
        else:
            self._active_state = active_state
        
        self._state = self._pin.value()
        
        self._when_activated = None
        self._when_deactivated = None
        
        self.was_pressed = False
        
        # setup interupt
        self._pin.irq(self._pin_change, Pin.IRQ_RISING | Pin.IRQ_FALLING)
        
    def _state_to_value(self, state):
        return int(bool(state) == self._active_state)
    
    def _read(self):
        return self._state_to_value(self._state)

    def _pin_change(self, p):
        # turn off the interupt
        p.irq(handler=None)
        
        last_state = p.value()
        
        if self._bounce_time is not None:
            # wait for stability
            stop = ticks_ms() + (self._bounce_time * 1000)
            while ticks_ms() < stop:
                # keep checking, reset the stop if the value changes
                if p.value() != last_state:
                    # War im Original fehlerhaft
                    # stop = ticks_ms() + self._bounce_time
                    stop = ticks_ms() + (self._bounce_time * 1000)
                    last_state = p.value()
        
        # re-enable the interupt
        p.irq(self._pin_change, Pin.IRQ_RISING | Pin.IRQ_FALLING)
        
        # did the value actually changed? 
        if self._state != last_state:
            # set the state
            self._state = self._pin.value()
            
            if self._state == 1:
                self.was_pressed = True
            
            # manage call backs
            callback_to_run = None
            if self.value and self._when_activated is not None:
                callback_to_run = self._when_activated
                    
            elif not self.value and self._when_deactivated is not None:
                callback_to_run = self._when_deactivated
            
            if callback_to_run is not None:
                
                def schedule_callback(callback):
                    callback()
            
                try:
                    schedule(schedule_callback, callback_to_run)
                    
                except RuntimeError as e:
                    if str(e) == "schedule queue full":
                        raise EventFailedScheduleQueueFull(
                            "{} - {} not run due to the micropython schedule being full".format(
                                str(self), callback_to_run.__name__))
                    else:
                        raise e

    @property
    def is_active(self):
        return bool(self.value)

    @property
    def is_inactive(self):
        return not bool(self.value)
    
    @property
    def when_activated(self):
        return self._when_activated
    
    @when_activated.setter
    def when_activated(self, value):
        self._when_activated = value
        
    @property
    def when_deactivated(self):
        return self._when_deactivated
    
    @when_activated.setter
    def when_deactivated(self, value):
        self._when_deactivated = value
    
    def close(self):
        self._pin.irq(handler=None)
        self._pin = None

class Switch(DigitalInputDevice):
    def __init__(self, pin, pull_up=True, bounce_time=0.02):
        super().__init__(pin=pin, pull_up=pull_up, bounce_time=bounce_time)

Switch.is_closed = Switch.is_active
Switch.is_open = Switch.is_inactive
Switch.when_closed = Switch.when_activated
Switch.when_opened = Switch.when_deactivated

class Button(Switch):
    pass

Button.is_pressed = Button.is_active
Button.is_released = Button.is_inactive
Button.when_pressed = Button.when_activated
Button.when_released = Button.when_deactivated