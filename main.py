import pygame
import random

pygame.init()


class Algorithm:
    def __init__(self, key=False):
        algorithms = {
            "Bubble Sort": self.bubbleSort,
            "Insertion Sort": self.insertionSort,
        }
        key_to_name = {pygame.K_b: "Bubble Sort", pygame.K_i: "Insertion Sort"}
        self.keys = key_to_name.keys()
        if not key:
            key = list(self.keys)[0]
        name = key_to_name[key]
        self.name = name
        self.algo = algorithms[name]

    def getName(self):
        return self.name

    def getGen(self):
        return self.gen

    def getKeys(self):
        return self.keys

    def setGen(self, screen):
        self.screen = screen
        lst = screen.getList()
        self.gen = self.algo(lst, screen.getAscending())

    def runDrawList(self):
        self.screen.drawList(clear_bg=True)

    def bubbleSort(self, lst, ascending):
        for i in range(len(lst) - 1):
            for j in range(len(lst) - 1 - i):
                num1 = lst[j]
                num2 = lst[j + 1]
                if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
                    self.runDrawList()
                    yield True

    def insertionSort(self, lst, ascending):
        for i in range(1, len(lst)):
            current = lst[i]
            while True:
                ascending_sort = i > 0 and lst[i - 1] > current and ascending
                descending_sort = i > 0 and lst[i - 1] < current and not ascending
                if not ascending_sort and not descending_sort:
                    break
                lst[i], lst[i - 1] = lst[i - 1], current
                i -= 1
                self.runDrawList()
                yield True


class Screen:
    def __init__(self, width, height, n, algo):
        self.width = width
        self.height = height
        self.side_pad = width / 8
        self.top_pad = height / 4
        self.n = n
        self.ascending = True
        self.window = pygame.display.set_mode((width, height))

        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.genList()
        self.draw(algo)

    def getList(self):
        return self.lst

    def getAscending(self):
        return self.ascending

    def setAscending(self, ascending):
        self.ascending = ascending

    def genList(self):
        lst = [random.randint(0, 100) for _ in range(self.n)]
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.bar_width = (self.width - self.side_pad) // len(lst)
        self.bar_height = (self.height - self.top_pad) // (max(lst) - min(lst))
        self.start_x = self.side_pad // 2

    def draw(self, algo):
        self.window.fill((0, 0, 0))
        # TODO improve UI
        controls = [
            "SPACE: Play/Pause Sorting",
            "R: Reset",
            "A: Ascending",
            "D: Descending",
            "I: Insertion Sort",
            "B: Bubble Sort",
        ]
        for i, control in enumerate(controls):
            color = 255, 255, 255
            if control[0] == "A" and self.ascending:
                color = 0, 255, 255
            if control[0] == "D" and not self.ascending:
                color = 0, 255, 255
            if control[3:] == algo.getName():
                color = 255, 0, 255

            self.window.blit(
                pygame.font.SysFont("helvetica", 16).render(
                    control,
                    1,
                    color,
                ),
                (10, 10 + 20 * i),
            )

        self.drawList()

    def drawList(self, clear_bg=False):
        if clear_bg:
            pygame.draw.rect(
                self.window,
                (0, 0, 0),
                (
                    self.side_pad // 2,
                    self.top_pad,
                    self.width - self.side_pad,
                    self.height,
                ),
            )

        list_set = list(set(self.lst))
        for i, val in enumerate(self.lst):
            x = self.start_x + i * self.bar_width
            y = self.height - (val - self.min_val) * self.bar_height
            color = (
                (list_set.index(val) + 1) / len(list_set) * 255,
                (sorted(list_set, reverse=True).index(val) + 1) / len(list_set) * 255,
                255,
            )
            pygame.draw.rect(self.window, color, (x, y, self.bar_width, self.height))
        pygame.display.update()


# FIXME padding needs to scale
def main(width=800, height=600, n=100):
    algo = Algorithm()
    screen = Screen(width, height, n, algo)
    sorting = False
    clock = pygame.time.Clock()
    while True:
        # TODO speed slider
        clock.tick(120)
        if sorting:
            try:
                next(algo.getGen())
            except StopIteration:
                screen.drawList(clear_bg=True)
                sorting = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_r:
                    screen.genList()
                    sorting = False
                elif key == pygame.K_SPACE:
                    sorting = False if sorting else True
                elif key == pygame.K_a:
                    screen.setAscending(True)
                elif key == pygame.K_d:
                    screen.setAscending(False)
                if key in algo.getKeys():
                    algo = Algorithm(key)
                algo.setGen(screen)
                screen.draw(algo)


if __name__ == "__main__":
    main()
