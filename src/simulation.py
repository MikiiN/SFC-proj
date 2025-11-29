import random


class Simulator:
    CLOSED_VALVE = 0.0
    OPENED_VALVE = 1.0
    NORMAL_PRESSURE = 1.0
    INIT_WATER_TEMPERATURE = 23.0

    def __init__(
            self,
            hot_water_temperature: float = 80.0,
            cold_water_temperature: float = 10.0,
            lower_pressure_chance: float = 0.1,
            lower_pressure: float = 0.6,
            buffer_size: int = 2,
            start_fault_time: int = None,
            end_fault_time: int = None
    ):
        self.hot_water_temp = hot_water_temperature
        self.cold_water_temp = cold_water_temperature
        self.lower_pressure = lower_pressure
        self.lower_pressure_chance = lower_pressure_chance
        self.hot_valve = self.CLOSED_VALVE
        self.cold_valve = self.CLOSED_VALVE
        self.buffer_size = buffer_size
        self.water_buffer = [self.INIT_WATER_TEMPERATURE] * buffer_size
        self.start_fault_time = start_fault_time
        self.end_fault_time = end_fault_time


    def _check_valve(self, valve_value):
        return valve_value >= self.CLOSED_VALVE and valve_value <= self.OPENED_VALVE


    def step(self, time, hot_valve = None, cold_valve = None):
        if hot_valve != None:
            self.hot_valve = hot_valve
        if cold_valve != None:
            self.cold_valve = cold_valve

        if self.hot_valve == self.CLOSED_VALVE and self.cold_valve == self.CLOSED_VALVE:
            return 0.0, 0.0
        
        percentage_chance = int(self.lower_pressure_chance * 100)
        if self.start_fault_time == None:
            fault = random.randint(0, 100) in range(percentage_chance)
            cold_flow = self.cold_valve * (self.lower_pressure if fault else self.NORMAL_PRESSURE)
        else:
            cold_flow = self.cold_valve * (
                self.lower_pressure if time >= self.start_fault_time and time <= self.end_fault_time else self.NORMAL_PRESSURE
            )
        hot_flow = self.hot_valve * self.NORMAL_PRESSURE
        new_temp = (cold_flow*self.cold_water_temp + hot_flow*self.hot_water_temp) / (cold_flow + hot_flow)
        new_flow = hot_flow + cold_flow
        self.water_buffer.append(new_temp)
        return new_flow, self.water_buffer.pop(0)