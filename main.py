import os, sys, collections
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def generate_prefix_tree(patterns):
    trie_children = [{}]
    next_node_id = 1
    output_lines = []

    for pattern in patterns:
        node = 0
        for ch in pattern:
            if ch in trie_children[node]:
                node = trie_children[node][ch]
            else:
                trie_children[node][ch] = next_node_id
                trie_children.append({})
                output_lines.append(f"{node}->{next_node_id}:{ch}")
                node = next_node_id
                next_node_id += 1

    return trie_children, output_lines

def entering(text, patterns):
    trie_children, output_lines = generate_prefix_tree(patterns)
    pattern_outputs = [[] for _ in range(len(trie_children))]

    for pid, pat in enumerate(patterns):
        node = 0
        for ch in pat:
            node = trie_children[node][ch]
        pattern_outputs[node].append(pid)

    fail = [0] * len(trie_children)
    queue = collections.deque()
    for ch, child in trie_children[0].items():
        fail[child] = 0
        queue.append(child)

    while queue:
        node = queue.popleft()
        for ch, child in trie_children[node].items():
            queue.append(child)
            f = fail[node]
            while f and ch not in trie_children[f]:
                f = fail[f]
            fail[child] = trie_children[f].get(ch, 0)
            pattern_outputs[child].extend(pattern_outputs[fail[child]])

    node = 0
    result_set = set()
    for i, ch in enumerate(text):
        while node and ch not in trie_children[node]:
            node = fail[node]
        node = trie_children[node].get(ch, 0)
        for pat_id in pattern_outputs[node]:
            start = i - len(patterns[pat_id]) + 1
            if start >= 0:
                result_set.add(start)

    result = sorted(result_set)
    if result:
        output_lines.append(" ".join(map(str, result)))

    return output_lines

def solve(task_type):
    with open('input.dat', 'r') as f:
        raw_lines = f.read().splitlines()
    data = [line.strip() for line in raw_lines if line.strip()]

    if task_type == 1:
        patterns = data[1:] if len(data) > 1 else []
        _, output_lines = generate_prefix_tree(patterns)
    elif task_type == 2:
        text = data[0]
        n = int(data[1])
        patterns = data[2:2+n]
        output_lines = entering(text, patterns)

    else:
        return

    with open('output.dat', 'w') as fout:
        for line in output_lines:
            fout.write(line + "\n")
    print("Файл output.dat успішно створено.")

if __name__ == '__main__':
    print("Виберіть тип задачі:")
    print("1 – Побудова префіксного дерева")
    print("2 – Всi входження множини шаблонiв в текстi (за допомогою префiксного дерева)")
    try:
        choice = int(input().strip())
    except ValueError:
        print("Неправильне значення.")
        sys.exit(1)

    solve(choice)
