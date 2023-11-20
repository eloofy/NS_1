import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle


class IntersectionAreaPlotter:
    def __init__(
        self,
        a,
        b,
        A,
        B,
        y1_min,
        y1_max,
        c,
        Y,
        G,
        y2_min,
        y2_max,
        x1_min,
        x1_max,
        x2_min,
        x2_max,
    ):
        """
        Initialize the IntersectionAreaPlotter with given parameters.

        Parameters:
            a, b, A, B (float): Coefficients for the first equation y1.
            y1_min, y1_max (float): Minimum and maximum values for y1.
            c, Y, G (float): Coefficients for the second equation y2.
            y2_min, y2_max (float): Minimum and maximum values for y2.
            x1_min, x1_max, x2_min, x2_max (float): Constraints for x1 and x2.
        """
        self.a, self.b, self.A, self.B = a, b, A, B
        self.y1_min, self.y1_max = y1_min, y1_max
        self.c, self.Y, self.G = c, Y, G
        self.y2_min, self.y2_max = y2_min, y2_max
        self.x1_min, self.x1_max, self.x2_min, self.x2_max = (
            x1_min,
            x1_max,
            x2_min,
            x2_max,
        )

        self.generate_grid()

    def generate_grid(self):
        """
        Generate a grid of x1 and x2 values and calculate corresponding y1 and y2 values.
        """
        x1_values = np.linspace(0, 10, 1000)
        x2_values = np.linspace(0, 10, 1000)
        self.x1, self.x2 = np.meshgrid(x1_values, x2_values)

        self.y1 = self.get_y1()
        self.y2 = self.get_y2()

        self.find_intersection()

    def get_y1(self):
        """
        Get y1 values based on the equation y1 = a * x1**A + b * x2**B.
        """
        return self.a * self.x1**self.A + self.b * self.x2**self.B

    def get_y2(self):
        """
        Get y2 values based on the equation y2 = c * x1**Y * x2**G.
        """
        return self.c * self.x1**self.Y * self.x2**self.G

    def find_intersection(self):
        """
        Find the intersection points within the given constraints.
        """
        intersection = np.logical_and(
            (self.y1 >= self.y1_min) & (self.y1 <= self.y1_max),
            (self.y2 >= self.y2_min) & (self.y2 <= self.y2_max),
        )
        self.x1_intersection = self.x1[intersection]
        self.x2_intersection = self.x2[intersection]

    def plot_intersection_area(self):
        """
        Plot the intersection area with contours and rectangles.
        """
        plt.figure(figsize=(8, 8))

        plt.contour(
            self.x1,
            self.x2,
            self.y1,
            levels=[self.y1_min, self.y1_max],
            colors=["blue", "blue"],
            alpha=0.7,
        )
        plt.contour(
            self.x1,
            self.x2,
            self.y2,
            levels=[self.y2_min, self.y2_max],
            colors=["red", "red"],
            alpha=0.7,
        )

        rectangle = Rectangle(
            (self.x1_min, self.x2_min),
            self.x1_max - self.x1_min,
            self.x2_max - self.x2_min,
            linewidth=2,
            edgecolor="black",
            facecolor="grey",
            alpha=0.6,
        )
        plt.gca().add_patch(rectangle)

        rectangle_outline = Rectangle(
            (self.x1_min, self.x2_min),
            self.x1_max - self.x1_min,
            self.x2_max - self.x2_min,
            linewidth=2,
            edgecolor="black",
            facecolor="none",
            zorder=20,
        )
        plt.gca().add_patch(rectangle_outline)

        plt.fill_between(
            self.x1_intersection,
            self.x2_intersection,
            self.x2_intersection,
            color="green",
        )

        legend_lines = [
            Line2D([0], [0], color="blue", label="y1(min, max)"),
            Line2D([0], [0], color="red", label="y2(min, max)"),
            Line2D([0], [0], color="green", label="ОБР"),
            Line2D([0], [0], color="black", label="РО"),
        ]

        percentage_area = self.calculate_percentage_area()
        percentage_text = f"Intersection Area: {percentage_area:.2f}%"
        plt.text(
            0.5,
            -0.1,
            percentage_text,
            horizontalalignment="center",
            verticalalignment="center",
            transform=plt.gca().transAxes,
            fontsize=12,
            bbox=dict(facecolor="white", edgecolor="white", boxstyle="round,pad=0.5"),
        )

        plt.legend(handles=legend_lines)
        plt.xlabel("x1")
        plt.ylabel("x2")
        plt.show()

    def calculate_percentage_area(self):
        """
        Calculate the percentage area of intersection within the given constraints.
        """
        points = np.array(
            [[x1, y1] for x1, y1 in zip(self.x1_intersection, self.x2_intersection)]
        )
        inside_points = points[
            (points[:, 0] >= self.x1_min)
            & (points[:, 0] <= self.x1_max)
            & (points[:, 1] >= self.x2_min)
            & (points[:, 1] <= self.x2_max)
        ]

        square_area = (
            (self.x1_max - self.x1_min) * (self.x2_max - self.x2_min) * 10 * 1000
        )

        return (inside_points.shape[0] / square_area) * 100


if __name__ == "__main__":
    plotter = IntersectionAreaPlotter(
        a=1,
        b=2,
        A=2,
        B=3,
        y1_min=5,
        y1_max=15,
        c=0.5,
        Y=1,
        G=2,
        y2_min=2,
        y2_max=10,
        x1_min=1,
        x1_max=2,
        x2_min=1,
        x2_max=2,
    )

    plotter.plot_intersection_area()
