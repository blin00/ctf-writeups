def dff(id, c, d, q):
    gates = []
    c_neg = f'{id}_1^'
    gates.append((c_neg, c, c))
    gates.append((f'{id}_2^', d, c_neg))
    gates.append((f'{id}_3', f'{id}_2^', c_neg))
    gates.append((f'{id}_4', c_neg, c_neg))
    gates.append((f'{id}_5', f'{id}_2^', f'{id}_6^'))
    gates.append((f'{id}_6^', f'{id}_3', f'{id}_5'))
    gates.append((f'{id}_7^', f'{id}_4', f'{id}_5'))
    gates.append((f'{id}_8^', f'{id}_4', f'{id}_7^'))
    gates.append((q, f'{id}_7^', f'{id}_9^'))
    gates.append((f'{id}_9^', f'{id}_8^', q))
    return gates
