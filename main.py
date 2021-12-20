import pygame
import random

pygame.init()


class DrawInformation:
    def __init__(self, width, height, n):
        self.width = width
        self.height = height
        self.side_pad = width / 8
        self.top_pad = height / 4
        self.n = n
        self.window = pygame.display.set_mode((width, height))

        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.genList()

    def genList(self):
        lst = [random.randint(0, 100) for _ in range(self.n)]
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.bar_width = (self.width - self.side_pad) // len(lst)
        self.bar_height = (self.height - self.top_pad) // (max(lst) - min(lst))
        self.start_x = self.side_pad // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill((0, 0, 0))
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
        if control[0] == "A" and ascending:
            color = 0, 255, 255
        if control[0] == "D" and not ascending:
            color = 0, 255, 255
        if control[3:] == algo_name:
            color = 255, 0, 255

        draw_info.window.blit(
            pygame.font.SysFont("helvetica", 16).render(
                control,
                1,
                color,
            ),
            (10, 10 + 20 * i),
        )

    drawList(draw_info)


def drawList(draw_info, clear_bg=False):
    if clear_bg:
        pygame.draw.rect(
            draw_info.window,
            (0, 0, 0),
            (
                draw_info.side_pad // 2,
                draw_info.top_pad,
                draw_info.width - draw_info.side_pad,
                draw_info.height,
            ),
        )

    list_set = list(set(draw_info.lst))
    for i, val in enumerate(draw_info.lst):
        x = draw_info.start_x + i * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.bar_height
        color = (
            (list_set.index(val) + 1) / len(list_set) * 255,
            (sorted(list_set, reverse=True).index(val) + 1) / len(list_set) * 255,
            255,
        )
        pygame.draw.rect(
            draw_info.window, color, (x, y, draw_info.bar_width, draw_info.height)
        )
    pygame.display.update()


def bubbleSort(draw_info, ascending):
    lst = draw_info.lst

    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                drawList(draw_info, True)
                yield True


def insertionSort(draw_info, ascending):
    lst = draw_info.lst
    for i in range(1, len(lst)):
        current = lst[i]
        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending
            if not ascending_sort and not descending_sort:
                break
            lst[i], lst[i - 1] = lst[i - 1], current
            i -= 1
            drawList(draw_info, True)
            yield True


# FIXME padding needs to scale
def main(width=800, height=600, n=100):
    algo_names = {bubbleSort: "Bubble Sort", insertionSort: "Insertion Sort"}
    algo_switches = {pygame.K_b: bubbleSort, pygame.K_i: insertionSort}
    algo = list(algo_names.keys())[0]
    algo_name = algo_names[algo]
    algo_gen = None

    sorting = False
    ascending = True

    draw_info = DrawInformation(width, height, n)
    clock = pygame.time.Clock()
    draw(draw_info, algo_name, ascending)
    while True:
        clock.tick(120)
        if sorting:
            try:
                next(algo_gen)
            except StopIteration:
                drawList(draw_info, clear_bg=True)
                sorting = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                key = event.key
                if key == pygame.K_r:
                    draw_info.genList()
                    sorting = False
                elif key == pygame.K_SPACE:
                    sorting = False if sorting else True
                elif key == pygame.K_a:
                    ascending = True
                elif key == pygame.K_d:
                    ascending = False
                elif key in algo_switches.keys():
                    algo = algo_switches[key]
                    algo_name = algo_names[algo]
                algo_gen = algo(draw_info, ascending)
                draw(draw_info, algo_name, ascending)


if __name__ == "__main__":
    main()
