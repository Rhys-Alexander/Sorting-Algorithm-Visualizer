import pygame
import random
from math import ceil

pygame.init()


class Screen:
    def __init__(self, size):
        self.bars = 50
        self.tick = 80
        self.width = size // 2 * 3
        self.height = size
        self.top_pad = self.height / 4
        self.font_size = self.height // 20
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.setAscending()
        self.setAlgo()
        self.genList()
        self.update()

    def genList(self):
        self.list = [random.randint(1, 100) for _ in range(self.bars)]
        self.len_list = len(self.list)
        self.sorted_list = sorted(self.list)
        self.reverse_list = sorted(self.list, reverse=True)
        self.bar_spacing = self.width / self.len_list
        self.bar_width = ceil(self.bar_spacing)
        self.bar_height = (self.height - self.top_pad) // max(self.list)

    def setTick(self, speed):
        self.tick = speed

    def getTick(self):
        return self.tick

    def changeTick(self, up):
        if up and self.tick < 160:
            self.tick *= 2
        elif not up and self.tick > 5:
            self.tick //= 2

    def changeBars(self, up):
        if up and self.bars < 200:
            self.bars += 10
        elif not up and self.bars > 10:
            self.bars -= 10
        self.genList()

    # Visualization
    def update(self):
        self.gen = self.algo()
        self.window.fill((0, 0, 0))
        titles1 = [
            f"ARROWS - {self.bars} Bars  {self.tick} Tick",
            "SPACE - Play/Pause",
            "R - Reset",
        ]
        for i, title in enumerate(titles1):
            self.window.blit(
                pygame.font.Font(None, self.font_size).render(
                    title,
                    1,
                    (255, 255, 255),
                ),
                (10, 10 + self.font_size * i),
            )

        titles2 = [
            "A - Ascending",
            "D - Descending",
        ]
        for i, title in enumerate(titles2):
            color = 255, 255, 255
            if title[0] == "A" and self.ascending:
                color = 0, 255, 255
            if title[0] == "D" and not self.ascending:
                color = 0, 255, 255

            self.window.blit(
                pygame.font.Font(None, self.font_size).render(
                    title,
                    1,
                    color,
                ),
                (self.width // 2, 10 + self.font_size * i),
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
                (self.width / 4 * 3, 10 + self.font_size * i),
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
        for i, val in enumerate(self.list):
            x = i * self.bar_spacing
            y = self.height - val * self.bar_height
            color = (
                (self.sorted_list.index(val) + 1) / self.len_list * 255,
                (self.reverse_list.index(val) + 1) / self.len_list * 255,
                255,
            )
            pygame.draw.rect(
                self.window,
                color,
                (x, y, self.bar_width, self.height),
            )
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

    def getGen(self):
        return self.gen

    def getAlgoKeys(self):
        return self.algo_keys

    # Algorithms
    def bubbleSort(self):
        for i in range(self.len_list - 1):
            for j in range(self.len_list - 1 - i):
                num1 = self.list[j]
                num2 = self.list[j + 1]
                if (num1 > num2 and self.ascending) or (
                    num1 < num2 and not self.ascending
                ):
                    self.list[j], self.list[j + 1] = self.list[j + 1], self.list[j]
                    self.drawList(clear_bg=True)
                    yield True

    def insertionSort(self):
        for i in range(1, self.len_list):
            current = self.list[i]
            while True:
                ascending_sort = i > 0 and self.list[i - 1] > current and self.ascending
                descending_sort = (
                    i > 0 and self.list[i - 1] < current and not self.ascending
                )
                if not ascending_sort and not descending_sort:
                    break
                self.list[i], self.list[i - 1] = self.list[i - 1], current
                i -= 1
                self.drawList(clear_bg=True)
                yield True

    # TODO add Merge Sort
    # TODO add Heap Sort
    # TODO add Quick Sort


def main(size=600):
    sorting = False
    screen = Screen(size)
    clock = pygame.time.Clock()
    while True:
        clock.tick(screen.getTick())
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
                elif key == pygame.K_LEFT:
                    screen.changeBars(False)
                    sorting = False
                elif key == pygame.K_RIGHT:
                    screen.changeBars(True)
                    sorting = False
                elif key == pygame.K_DOWN:
                    screen.changeTick(False)
                elif key == pygame.K_UP:
                    screen.changeTick(True)
                if key in screen.getAlgoKeys():
                    screen.setAlgo(key)
                screen.update()


if __name__ == "__main__":
    main()
