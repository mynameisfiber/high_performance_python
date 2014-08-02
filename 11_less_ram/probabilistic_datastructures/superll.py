from ll import LL
import math


class SuperLL(LL):
    NMAX = 1000000000

    def __len__(self):
        # truncation
        register_num1 = int(self.num_registers * 0.7)
        registers_truncated1 = sorted(
            h.counter for h in self.registers)[:register_num1]

        # restriction
        B = math.ceil(
            math.log(self.NMAX / self.num_registers) / math.log(2.0) + 3)
        registers_truncated2 = [v for v in registers_truncated1 if v <= B]
        register_num2 = len(registers_truncated2)
        register_sum = sum(registers_truncated2)

        alpha = 0.7213 / (1.0 + 1.079 / register_num2)
        return 2 ** (float(register_sum) / register_num2) * \
            register_num2 * alpha
