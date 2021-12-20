import pygame
import random

pygame.init()


class Screen:
    def __init__(self, size, n):
        width, height = size // 2 * 3, size
        print(width, height)
        self.width = width
        self.height = height
        self.top_pad = height / 4
        self.font_size = height // 20
        self.n = n
        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.setAscending()
        self.setAlgo()
        self.genList()
        self.draw()

    def genList(self):
        lst = [random.randint(0, 100) for _ in range(self.n)]
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.bar_width = self.width // len(lst)
        self.bar_height = (self.height - self.top_pad) // (max(lst) - min(lst))

    # Visualization
    def draw(self):
        self.window.fill((0, 0, 0))
        # TODO use buttons
        controls = [
            "SPACE - Play/Pause",
            "R - Reset",
            "A - Ascending",
            "D - Descending",
        ]
        for i, control in enumerate(controls):
            color = 255, 255, 255
            if control[0] == "A" and self.ascending:
                color = 0, 255, 255
            if control[0] == "D" and not self.ascending:
                color = 0, 255, 255

            self.window.blit(
                pygame.font.Font(None, self.font_size).render(
                    control,
                    1,
                    color,
                ),
                (10, 10 + self.font_size * i),
            )

        algorithms = [f"{name[0]} - {name}" for name in self.algorithms.keys()]
        for i, algo in enumerate(algorithms):
            color = 255, 255, 255
            if algo[0] == self.algo_name[0]:
                color = 255, 0, 255

            self.window.blit(
                pygame.font.Font(None, self.font_size).render(
                    algo,
                    1,
                    color,
                ),
                (self.width // 2, 10 + self.font_size * i),
            )

        self.drawList()

    def drawList(self, clear_bg=False):
        if clear_bg:
            pygame.draw.rect(
                self.window,
                (0, 0, 0),
                (
                    0,
                    self.top_pad,
                    self.width,
                    self.height,
                ),
            )

        list_set = list(set(self.lst))
        for i, val in enumerate(self.lst):
            x = i * self.bar_width
            y = self.height - (val - self.min_val) * self.bar_height
            color = (
                (list_set.index(val) + 1) / len(list_set) * 255,
                (sorted(list_set, reverse=True).index(val) + 1) / len(list_set) * 255,
                255,
            )
            pygame.draw.rect(self.window, color, (x, y, self.bar_width, self.height))
        pygame.display.update()

    # Algorithm Methods
    def setAscending(self, ascending=True):
        self.ascending = ascending

    def setAlgo(self, key=False):
        self.algorithms = {
            "Bubble Sort": self.bubbleSort,
            "Insertion Sort": self.insertionSort,
        }
        key_to_name = {pygame.K_b: "Bubble Sort", pygame.K_i: "Insertion Sort"}
        self.algo_keys = key_to_name.keys()
        if not key:
            key = list(self.algo_keys)[0]
        name = key_to_name[key]
        self.algo_name = name
        self.algo = self.algorithms[name]

    def setGen(self):
        self.gen = self.algo(self.lst, self.ascending)

    def getGen(self):
        return self.gen

    def getAlgoKeys(self):
        return self.algo_keys

    # Algorithms
    def bubbleSort(self, lst, ascending):
        for i in range(len(lst) - 1):
            for j in range(len(lst) - 1 - i):
                num1 = lst[j]
                num2 = lst[j + 1]
                if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
                    self.drawList(clear_bg=True)
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
                self.drawList(clear_bg=True)
                yield True

    # TODO add algorithms


# FIXME colors bug out on low bar numbers
def main(size=600, n=50):
    # TODO number of bars slider
    n = 20
    sorting = False
    screen = Screen(size, n)
    clock = pygame.time.Clock()
    # TODO tick slider
    tick = 120
    while True:
        # TODO speed slider
        clock.tick(tick)
        if sorting:
            try:
                next(screen.getGen())
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
                if key in screen.getAlgoKeys():
                    screen.setAlgo(key)
                screen.setGen()
                screen.draw()


if __name__ == "__main__":
    main()
