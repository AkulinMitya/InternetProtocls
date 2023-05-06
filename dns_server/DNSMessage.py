class DNSMessage:
    def __init__(self, id, qr, opcode, aa, tc, rd, ra, z, rcode, questions, answers):
        self.id = id
        self.qr = qr
        self.opcode = opcode
        self.aa = aa
        self.tc = tc
        self.rd = rd
        self.ra = ra
        self.z = z
        self.rcode = rcode
        self.questions = questions
        self.answers = answers

    def __str__(self):
        question_str = "\n".join(f"{q[0]} ({q[1]})" for q in self.questions)
        answer_str = "\n".join(f"{a[0]}: {a[1]}" for a in self.answers)
        return f"Questions:\n{question_str}\nAnswers:\n{answer_str}"
