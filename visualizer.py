import pygame
import random
from math import ceil


class Visualizer:
    pygame.init()

    def __init__(self, size=720):
        self.sorting = False
        self.ascending = True
        self.bars = 64
        self.tick = 64
        self.width = size // 2 * 3
        self.height = size
        self.top_pad = self.height / 4
        self.font_size = self.height // 24
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.setAlgo()
        self.genList()
        self.update()
        self.gen = self.algo()

    def genList(self):
        self.list = [100 / self.bars * (i + 1) for i in range(self.bars)]
        random.shuffle(self.list)
        self.bar_spacing = self.width / self.bars
        self.bar_width = ceil(self.bar_spacing)
        self.bar_height = (self.height - self.top_pad) // 100

    def changeTick(self, up):
        if up and self.tick < 256:
            self.tick *= 2
        elif not up and self.tick > 4:
            self.tick //= 2

    def changeBars(self, up):
        if up and self.bars < 256:
            self.bars *= 2
        elif not up and self.bars > 4:
            self.bars //= 2
        self.genList()

    def setAlgo(self, key=False):
        self.algorithms = {
            pygame.K_b: ("Bubble Sort", self.bubbleSort),
            pygame.K_i: ("Insertion Sort", self.insertionSort),
            pygame.K_m: ("Merge Sort", self.mergeSort),
            pygame.K_q: ("Quick Sort", self.quickSort),
            pygame.K_c: ("Crazy Sort", self.crazySort),
            pygame.K_s: ("Selection Sort", self.selectionSort),
        }
        if not key:
            key = list(self.algorithms.keys())[0]
        self.algo_name = self.algorithms[key][0]
        self.algo = self.algorithms[key][1]

    # Visualization
    def update(self):
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
                (self.width // 3, 10 + self.font_size * i),
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
                (self.width // 3 * 2, 10 + self.font_size * i),
            )

        algorithms = [
            f"{name[0]} - {name}" for name in (x for x, _ in self.algorithms.values())
        ]
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
                (10, 10 + self.font_size * i),
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
                val * 2.55,
                (100 - val) * 2.55,
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
        for i in range(self.bars - 1):
            for j in range(self.bars - 1 - i):
                num1 = self.list[j]
                num2 = self.list[j + 1]
                if (num1 > num2 and self.ascending) or (
                    num1 < num2 and not self.ascending
                ):
                    self.list[j], self.list[j + 1] = self.list[j + 1], self.list[j]
                    yield True

    def insertionSort(self):
        for i in range(1, self.bars):
            current = self.list[i]
            while True:
                ascending_sort = i > 0 and self.list[i - 1] > current and self.ascending
                descending_sort = (
                    i > 0 and self.list[i - 1] < current and not self.ascending
                )
                if not (ascending_sort or descending_sort):
                    break
                self.list[i], self.list[i - 1] = self.list[i - 1], current
                i -= 1
                yield True

    def selectionSort(self):
        for i in range(self.bars - 1):
            k = i
            for j in range(i + 1, self.bars):
                if (
                    self.list[j] < self.list[k]
                    and self.ascending
                    or self.list[j] > self.list[k]
                    and not self.ascending
                ):
                    k = j
            self.list[i], self.list[k] = self.list[k], self.list[i]
            yield True

    def mergeSort(self, start=0, end=False):
        if not end:
            end = self.bars
        if end - start > 1:
            mid = (start + end) // 2

            yield from self.mergeSort(start, mid)
            yield from self.mergeSort(mid, end)
            left = self.list[start:mid]
            right = self.list[mid:end]

            a = 0
            b = 0
            c = start

            while a < len(left) and b < len(right):
                if (left[a] < right[b] and self.ascending) or (
                    left[a] > right[b] and not self.ascending
                ):
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

    def quickSort(self, low=0, high=None):
        if high is None:
            high = self.bars - 1
        partition = self.quickSortPartition(low, high)
        while low < high:
            while True:
                try:
                    pi = next(partition)
                    break
                except StopIteration:
                    partition = self.quickSortPartition(low, high)
                    break
            if pi:
                if pi - low < high - pi:
                    yield from self.quickSort(low, pi - 1)
                    low = pi + 1
                else:
                    yield from self.quickSort(pi + 1, high)
                    high = pi - 1
            else:
                yield True

    def quickSortPartition(self, l, h):
        pivot = self.list[h]
        i = l - 1
        for j in range(l, h):
            if (self.list[j] <= pivot and self.ascending) or (
                self.list[j] > pivot and not self.ascending
            ):
                i = i + 1
                (self.list[i], self.list[j]) = (self.list[j], self.list[i])
                yield False

        (self.list[i + 1], self.list[h]) = (self.list[h], self.list[i + 1])
        yield i + 1

    def crazySort(self):
        while not (
            self.list == sorted(self.list)
            if self.ascending
            else self.list == sorted(self.list, reverse=True)
        ):
            random.shuffle(self.list)
            yield True

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
                    if key == pygame.K_SPACE:
                        self.sorting = False if self.sorting else True
                    elif key == pygame.K_DOWN:
                        self.changeTick(False)
                    elif key == pygame.K_UP:
                        self.changeTick(True)
                    else:
                        if key == pygame.K_r:
                            self.genList()
                            self.sorting = False
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
                        elif key in self.algorithms.keys():
                            self.setAlgo(key)
                        else:
                            continue
                        self.gen = self.algo()
                    self.update()


if __name__ == "__main__":
    Visualizer().run()
