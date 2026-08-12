import math

INPUT_SIZE = 7  # sin(t), cos(t), hip angle/velocity, knee angle/velocity, leg phase offset
HIDDEN_SIZE = 8
OUTPUT_SIZE = 2  # hip motor rate, knee motor rate

GENOME_LENGTH = (
    INPUT_SIZE * HIDDEN_SIZE + HIDDEN_SIZE + HIDDEN_SIZE * OUTPUT_SIZE + OUTPUT_SIZE
)
MAX_MOTOR_RATE = 3.0


def _unpack(weights):
    idx = 0
    w1 = []
    for _ in range(HIDDEN_SIZE):
        w1.append(weights[idx : idx + INPUT_SIZE])
        idx += INPUT_SIZE
    b1 = weights[idx : idx + HIDDEN_SIZE]
    idx += HIDDEN_SIZE
    w2 = []
    for _ in range(OUTPUT_SIZE):
        w2.append(weights[idx : idx + HIDDEN_SIZE])
        idx += HIDDEN_SIZE
    b2 = weights[idx : idx + OUTPUT_SIZE]
    return w1, b1, w2, b2


def forward(weights, inputs):
    """A tiny MLP: INPUT_SIZE -> HIDDEN_SIZE (tanh) -> OUTPUT_SIZE (tanh, scaled).

    weights is the flat genome; the same network is evaluated once per leg
    (with that leg's own angles/velocities), so evolution shapes one shared
    "brain" rather than a separate one per leg.
    """
    w1, b1, w2, b2 = _unpack(weights)
    hidden = [
        math.tanh(sum(w1[h][k] * inputs[k] for k in range(INPUT_SIZE)) + b1[h])
        for h in range(HIDDEN_SIZE)
    ]
    return [
        math.tanh(sum(w2[o][h] * hidden[h] for h in range(HIDDEN_SIZE)) + b2[o]) * MAX_MOTOR_RATE
        for o in range(OUTPUT_SIZE)
    ]
