import pygame
import random
from math import ceil


class Visualizer:
    pygame.init()

    def __init__(self, size=600):
        self.sorting = False
        self.ascending = True
        self.bars = 50
        self.tick = 80
        self.width = size // 2 * 3
        self.height = size
        self.top_pad = self.height / 4
        self.font_size = self.height // 20
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
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

    def setAlgo(self, key=False):
        self.algorithms = {
            "Bubble Sort": self.bubbleSort,
            "Insertion Sort": self.insertionSort,
            "Merge Sort": self.mergeSort,
        }
        key_to_name = {
            pygame.K_b: "Bubble Sort",
            pygame.K_i: "Insertion Sort",
            pygame.K_m: "Merge Sort",
        }
        self.algo_keys = key_to_name.keys()
        if not key:
            key = list(self.algo_keys)[0]
        name = key_to_name[key]
        self.algo_name = name
        self.algo = self.algorithms[name]

    # Visualization
    def update(self):
        self.gen = self.algo()
        self.window.fill((0, 0, 0))
        play_pause = "Pause" if self.sorting else "Play"
        titles1 = [
            f"ARROWS - {self.bars} Bars  {self.tick} Tick",
            f"SPACE - {play_pause}",
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
                yield True

    # TODO descending functionality https://www.geeksforgeeks.org/merge-sort/
    def mergeSort(self, start=0, end=False):
        if not end:
            end = self.len_list
        if end - start > 1:
            middle = (start + end) // 2

            yield from self.mergeSort(start, middle)
            yield from self.mergeSort(middle, end)
            left = self.list[start:middle]
            right = self.list[middle:end]

            a = 0
            b = 0
            c = start

            while a < len(left) and b < len(right):
                if left[a] < right[b]:
                    self.list[c] = left[a]
                    a += 1
                else:
                    self.list[c] = right[b]
                    b += 1
                c += 1
                yield True

            while a < len(left):
                self.list[c] = left[a]
                a += 1
                c += 1
                yield True

            while b < len(right):
                self.list[c] = right[b]
                b += 1
                c += 1
                yield True

            yield True

    # TODO Heap Sort https://www.geeksforgeeks.org/heap-sort/
    # TODO Quick Sort https://www.geeksforgeeks.org/quick-sort/
    # TODO check sort against https://clementmihailescu.github.io/Sorting-Visualizer/

    # Main function
    def run(self):
        clock = pygame.time.Clock()
        while True:
            clock.tick(self.tick)
            if self.sorting:
                try:
                    next(self.gen)
                    self.drawList(clear_bg=True)
                except StopIteration:
                    self.sorting = False
                    self.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    key = event.key
                    if key == pygame.K_r:
                        self.genList()
                        self.sorting = False
                    elif key == pygame.K_SPACE:
                        self.sorting = False if self.sorting else True
                    elif key == pygame.K_a:
                        self.ascending = True
                    elif key == pygame.K_d:
                        self.ascending = False
                    elif key == pygame.K_LEFT:
                        self.changeBars(False)
                        self.sorting = False
                    elif key == pygame.K_RIGHT:
                        self.changeBars(True)
                        self.sorting = False
                    elif key == pygame.K_DOWN:
                        self.changeTick(False)
                    elif key == pygame.K_UP:
                        self.changeTick(True)
                    elif key in self.algo_keys:
                        self.setAlgo(key)
                    self.update()


if __name__ == "__main__":
    Visualizer().run()
