from lexer import analyse_lexicale


class Parser:
    def __init__(self, expression):
        self.tokens = analyse_lexicale(expression)
        self.pos = 0
    # retourne le jeton actuellement pointé par self.pos
    def courant(self):
        return self.tokens[self.pos]

    def avancer(self):
        if self.pos < len(self.tokens) - 1:
            self.pos = self.pos + 1

    def erreur(self, attendu):
        t = self.courant()
        raise SyntaxError(
            "Erreur a la position " + str(t.position)
            + " : " + attendu
            + " attendu, " + t.nature + " trouve"
        )

    def accepter(self, nature):
        if self.courant().nature == nature:
            self.avancer()
        else:
            self.erreur(nature)

    def analyser(self):
        self.R()

        if self.courant().nature != "FIN":
            self.erreur("FIN")

        return True

    def R(self):
        self.T()
        self.R_prime()

    def R_prime(self):
        if self.courant().nature == "UNION":
            self.avancer()
            self.T()
            self.R_prime()

        elif self.courant().nature in [
            "PARENTHESE_FERMANTE", "FIN"
        ]:
            return

        else:
            self.erreur("UNION, ) ou FIN")

    def T(self):
        self.F()
        self.T_prime()

    def T_prime(self):
        if self.courant().nature in [
            "SYMBOLE",
            "MOT_VIDE",
            "PARENTHESE_OUVRANTE"
        ]:
            self.F()
            self.T_prime()

        elif self.courant().nature in [
            "UNION",
            "PARENTHESE_FERMANTE",
            "FIN"
        ]:
            return

        else:
            self.erreur("SYMBOLE, @, (, |, ) ou FIN")

    def F(self):
        self.A()
        self.F_prime()

    def F_prime(self):
        if self.courant().nature in [
            "ETOILE", "PLUS", "OPTIONNEL"
        ]:
            self.avancer()
            self.F_prime()

        elif self.courant().nature in [
            "SYMBOLE", "MOT_VIDE",
            "PARENTHESE_OUVRANTE",
            "UNION", "PARENTHESE_FERMANTE", "FIN"
        ]:
            return

        else:
            self.erreur("*, +, ?, SYMBOLE, @, (, |, ) ou FIN")

    def A(self):
        if self.courant().nature == "PARENTHESE_OUVRANTE":
            self.avancer()
            self.R()
            self.accepter("PARENTHESE_FERMANTE")

        elif self.courant().nature == "SYMBOLE":
            self.avancer()

        elif self.courant().nature == "MOT_VIDE":
            self.avancer()

        else:
            self.erreur("(, SYMBOLE ou @")


# Tests
expressions = ["a|b", "ab*", "(a|b)*", "a||b", "*a", "(ab"]

for exp in expressions:
    try:
        p = Parser(exp)
        p.analyser()
      
        print(exp, ": Expression valide")
    except (SyntaxError, ValueError) as e:
        print(exp, ":", e)
