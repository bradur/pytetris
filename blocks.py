import pygame


class Blocks(object):
    def __init__(self, size):

        self.size = size
        self.block = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        self.block.convert_alpha()

        self.colors = {
            "L": (233, 133, 33),  # Orange #E98521
            "Z": (233, 66, 66),   # Red    #E94242
            "S": (33, 233, 33),   # Green  #21E921
            "T": (133, 66, 133),  # Purple #854285
            "O": (233, 233, 66),  # Yellow #E9E942
            "J": (66, 66, 233),   # Blue   #4242E9
            "I": (66, 233, 233)   # Cyan   #42E9E9
        }

        # block.fill((33, 233, 33))  # green
        # block.fill((0, 0, 0))  # green
        # top horizontal
        pygame.draw.line(self.block, (0, 0, 0), (1, 0), (size-2, 0))
        # left vertical
        pygame.draw.line(self.block, (0, 0, 0), (0, 1), (0, size-2))
        pygame.draw.line(  # bottom horizontal
            self.block, (0, 0, 0),
            (1, size-1),
            (size-2, size-1)
        )
        pygame.draw.line(  # right vertical
            self.block, (0, 0, 0),
            (size-1, 1),
            (size-1, size-2)
        )

        self.b = self.block.copy()
        b = pygame.Surface((size-2, size-2))
        b.fill(self.colors["O"])
        self.b.blit(b, (1, 1))

        # Z tetromino
        b = pygame.Surface((size-2, size-2))
        b.fill(self.colors["Z"])
        self.block.blit(b, (1, 1))
        self.block_z = pygame.Surface((size*3, size*3), pygame.SRCALPHA, 32)
        self.block_z.convert_alpha()
        self.block_z.blit(self.block, (0, 0))
        self.block_z.blit(self.block, (size, 0))
        self.block_z.blit(self.block, (size, size))
        self.block_z.blit(self.block, (size*2, size))

        # S tetromino
        b = pygame.Surface((size-2, size-2))
        b.fill(self.colors["S"])
        self.block.blit(b, (1, 1))
        self.block_s = pygame.Surface((size*3, size*3), pygame.SRCALPHA, 32)
        self.block_s.convert_alpha()
        self.block_s.blit(self.block, (0, size))
        self.block_s.blit(self.block, (size, 0))
        self.block_s.blit(self.block, (size, size))
        self.block_s.blit(self.block, (size*2, 0))

        # T tetromino
        b = pygame.Surface((size-2, size-2))
        b.fill(self.colors["T"])  # purple
        self.block.blit(b, (1, 1))
        self.block_t = pygame.Surface((size*3, size*3), pygame.SRCALPHA, 32)
        self.block_t.convert_alpha()
        self.block_t.blit(self.block, (0, size))
        self.block_t.blit(self.block, (size, 0))
        self.block_t.blit(self.block, (size, size))
        self.block_t.blit(self.block, (size*2, size))

        # O tetromino
        b = pygame.Surface((size-2, size-2))
        b.fill(self.colors["O"])  # yellow
        self.block.blit(b, (1, 1))
        self.block_o = pygame.Surface((size*3, size*2), pygame.SRCALPHA, 32)
        self.block_o.convert_alpha()
        self.block_o.blit(self.block, (0, 0))
        self.block_o.blit(self.block, (0, size))
        self.block_o.blit(self.block, (size, 0))
        self.block_o.blit(self.block, (size, size))

        # J tetromino
        b = pygame.Surface((size-2, size-2))
        b.fill(self.colors["J"])  # blue
        self.block.blit(b, (1, 1))
        self.block_j = pygame.Surface((size*3, size*3), pygame.SRCALPHA, 32)
        self.block_j.convert_alpha()
        self.block_j.blit(self.block, (0, 0))
        self.block_j.blit(self.block, (0, size))
        self.block_j.blit(self.block, (size, size))
        self.block_j.blit(self.block, (size*2, size))

        # L tetromino
        b = pygame.Surface((size-2, size-2))
        b.fill(self.colors["L"])  # orange
        self.block.blit(b, (1, 1))
        self.block_l = pygame.Surface((size*3, size*3), pygame.SRCALPHA, 32)
        self.block_l.convert_alpha()
        self.block_l.blit(self.block, (0, size))
        self.block_l.blit(self.block, (size, size))
        self.block_l.blit(self.block, (size*2, size))
        self.block_l.blit(self.block, (size*2, 0))

        # I tetromino
        b = pygame.Surface((size-2, size-2))
        b.fill(self.colors["I"])  # cyan
        self.block.blit(b, (1, 1))
        self.block_i = pygame.Surface((size*4, size*4), pygame.SRCALPHA, 32)
        self.block_i.convert_alpha()
        self.block_i.blit(self.block, (0, size))
        self.block_i.blit(self.block, (size, size))
        self.block_i.blit(self.block, (size*2, size))
        self.block_i.blit(self.block, (size*3, size))
