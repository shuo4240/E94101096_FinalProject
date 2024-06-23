import flet as ft
import numpy as np
import matplotlib.pyplot as plt
import padasip as pa
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def main(page: ft.Page):
    
    page.window_width = 600
    page.window_height = 800
    
    select_filter = ft.Dropdown(
        label="Adaptive Filter",
        hint_text="Choose an adaptive filter",
        options=[
            ft.dropdown.Option("LMS"),
            ft.dropdown.Option("RLS"),
            ft.dropdown.Option("NLMS"),
        ],
        autofocus=True,
        width=250, 
    )
    coeff1 = ft.TextField(label="Coefficient1", width=150, value="2.0")
    coeff2 = ft.TextField(label="Coefficient2", width=150, value="0.1")
    coeff3 = ft.TextField(label="Coefficient3", width=150, value="4.0")
    coeff4 = ft.TextField(label="Coefficient4", width=150, value="0.5")
    n_field = ft.TextField(label="n (Dimension of input vector):", width=240, value="4")
    mu_field = ft.TextField(label="mu (Adaptation step size):", width=240, value="0.01")

    def plot_click(e):
        n = int(n_field.value)
        mu = float(mu_field.value)

        # 500個樣本
        N = 500

        # 代表噪音
        v = np.random.normal(0, 0.1*(slider.value+1), N)

        x = np.random.normal(0, 1, (N, n))
        d = float(coeff1.value) * x[:, 0] + float(coeff2.value) * x[:, 1] - float(coeff3.value) * x[:, 2] + float(coeff4.value) * x[:, 3] + v

        f = None
        if select_filter.value == "LMS":
            f = pa.filters.FilterLMS(n=n, mu=mu, w="random")
        elif select_filter.value == "RLS":
            f = pa.filters.FilterRLS(n=n, mu=mu)
        elif select_filter.value == "NLMS":
            f = pa.filters.FilterNLMS(n=n, mu=mu, w="random")


        y, e, w = f.run(d, x)

        root = tk.Tk()
        root.title("Filter Plot")

        # 顯示圖表
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
        ax1.set_title("Adaptation Process")
        ax1.set_xlabel("Sample Indexs")
        ax1.plot(d, "b", label="d : Target")
        ax1.plot(y, "g", label="y : Output")
        ax1.legend()

        plt.subplots_adjust(hspace=0.5)

        ax2.set_title("Filter Error")
        ax2.set_xlabel("Sample Indexs")
        ax2.plot(10 * np.log10(e ** 2), "r", label="Error (dB)")
        ax2.legend()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        root.mainloop()

    plot_btn = ft.FilledButton(text="Show Filter Plot", on_click=plot_click)

    def difference_click(e):
        n = int(n_field.value)
        mu = float(mu_field.value)

        # 500個樣本
        N = 500

        # 代表噪音
        v = np.random.normal(0, 0.1*(slider.value+1), N)

        x = np.random.normal(0, 1, (N, n))
        d = float(coeff1.value) * x[:, 0] + float(coeff2.value) * x[:, 1] - float(coeff3.value) * x[:, 2] + float(coeff4.value) * x[:, 3] + v

        # 濾波器
        f1 = pa.filters.FilterLMS(n=n, mu=mu, w="random")
        f2 = pa.filters.FilterRLS(n=n, mu=mu)
        f3 = pa.filters.FilterNLMS(n=n, mu=mu, w="random")

        y1, e1, w1 = f1.run(d, x)
        y2, e2, w2 = f2.run(d, x)
        y3, e3, w3 = f3.run(d, x)

        # 計算平均誤差
        avg_error_lms = np.mean(e1 ** 2)
        avg_error_rls = np.mean(e2 ** 2)
        avg_error_nlms = np.mean(e3 ** 2)
        print(avg_error_lms, avg_error_rls, avg_error_nlms)
        # 找到最小誤差
        min_error = min(avg_error_lms, avg_error_rls, avg_error_nlms)
        if min_error == avg_error_lms:
            recommended_filter = "LMS"
        elif min_error == avg_error_rls:
            recommended_filter = "RLS"
        else:
            recommended_filter = "NLMS"

        root = tk.Tk()
        root.title("Filter Plot")

        # 顯示圖表
        fig, ax = plt.subplots(figsize=(10, 7))

        ax.set_title("Compare Filter Error")
        ax.set_xlabel("Sample Indexs")
        ax.plot(10 * np.log10(e1 ** 2), "r", label="LMS Error (dB)")
        ax.plot(10 * np.log10(e2 ** 2), "g", label="RLS Error (dB)")
        ax.plot(10 * np.log10(e3 ** 2), "b", label="NLMS Error (dB)")
        ax.legend()

        # 在圖表下方顯示推薦的濾波器
        recommendation_label = tk.Label(root, text=f"Recommended Filter: {recommended_filter}", font=("Arial", 14))
        recommendation_label.pack()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        root.mainloop()
        
    difference_btn = ft.FilledButton(text="Show Three filter Error", on_click=difference_click, style=ft.ButtonStyle(bgcolor=ft.colors.RED,))


        
    icon_speak = ft.Draggable(group="voice", content=ft.Icon(name="RECORD_VOICE_OVER", size=20, color=ft.colors.WHITE))
    icon_mircophone = ft.Draggable(group="voice", content=ft.Icon(name="KEYBOARD_VOICE_ROUNDED", size=20, color=ft.colors.WHITE))
    
    
    def slider_change(e):
        t.value = f"The sound source is {5 - e.control.value} m away from the microphone"
        page.update()
    
    t = ft.Text()
    slider = ft.Slider(min=0, max=5, divisions=5, on_change=slider_change)



    page.add(
        select_filter,
        coeff1,
        coeff2,
        coeff3,
        coeff4,
        n_field,
        mu_field,
        slider,
        
        ft.Row(
            [
                ft.Container(
                    content=icon_speak,
                    width=30,
                    height=30,
                    bgcolor=ft.colors.BLUE,
                    border_radius=15,
                ),

                ft.Container(
                    content=t,
                    width=480,
                    height=30,
                    bgcolor=ft.colors.WHITE,
                ),

                ft.Container(
                    content=icon_mircophone,
                    width=30,
                    height=30,
                    bgcolor=ft.colors.BLUE,
                    border_radius=15,
                )
            ]
        ),
        plot_btn,
        difference_btn,

    )

ft.app(target=main)
