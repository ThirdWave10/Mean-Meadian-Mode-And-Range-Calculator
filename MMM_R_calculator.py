import random
from tkinter import messagebox

from tkinter import simpledialog
import statistics
import tkinter as tk
import numpy as np
import subprocess
import os

try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter
except ModuleNotFoundError:
    subprocess.run(["pip3", "install", "reportlab"])
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter

try:
    import matplotlib.pyplot as plt
except ModuleNotFoundError:
    subprocess.run(["pip3", "install", "matplotlib"])
    import matplotlib.pyplot as plt
except Exception:
    raise Exception






if not os.path.exists('number.txt'):
    with open("number.txt", "w") as file:
        file.write("0")

alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def cal_Outliers(data,q1,q3,iqr):
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    outliers = [x for x in data if x < Q1 - 1.5 * IQR or x > Q3 + 1.5 * IQR]
    return outliers


def cal_qs(data):
    length = len(data)
    data = sorted(data)
    first_half = data[:length//2]
    q1 = statistics.median(first_half)
    second_half = data[length//2:]
    q3 = statistics.median(second_half)
    iqr = q3 - q1
    return [q1, q3, iqr]

def text_gui():
    choice = ""
    data = []

    while True:
        choice = input("Please enter a data point or q to quit/get results or del to get rid of last input: ")

        # Check if the user entered a number
        if choice.isdigit() or isfloat(choice):
            data.append(float(choice))

        if "," in choice:
            list1 = choice.split(",")
            for i in list1:
                data.append(i)


        # Check if the user entered a product
        elif choice[0].isdigit() or isfloat(choice[0]):
            numbers_list = []

            for x in choice:

                if x.isdigit():
                    numbers_list.append(x)

                elif x == ".":
                    numbers_list.append(x)

                # Checks to see if the user has entered a times
                elif x == "x":
                    numbers = str(numbers_list)
                    numbers = numbers.replace(",", "")
                    numbers = numbers.replace(" ", "")
                    numbers = numbers.replace("[", "")
                    numbers = numbers.replace("]", "")
                    numbers = numbers.replace("'", "")

                    # Checks if numbers is a digit
                    if numbers.isdigit() or isfloat(numbers):
                        index = choice.index(x)
                        second_numbers = choice[index + 1:]

                        # Makes sure the rest of the numbers are digits
                        if second_numbers.isdigit():
                            numbers = numbers + " "
                            second_numbers = int(second_numbers)
                            product = numbers * second_numbers
                            product = product.split(" ")

                            # Once multiplied add them all to data
                            for x in product:
                                if isfloat(x):
                                    data.append(float(x))
                                else:
                                    break

                        else:
                            print("Second Number(s) is not a digit")
                    else:
                        print("Please enter a number")
                else:
                    print("Please enter a number or a product")

        # Finally, checks if the user wants to quit/get results
        else:
            if choice == "q" or choice == "Q" or choice == "quit":
                if len(data) > 1:
                    print("\n\n\n")
                    break
                else:
                    print("Please enter at least two data points")
                    continue
            if choice == "del":
                del (data[-1])
                print("Deleted last data point")

            print("Invalid input: Enter a number")

    cal_data = calculate_data(data)

    for x, y in cal_data.items():
        print(f"{x} = {y}")

    final_data = []
    for x in data:
        try:
            final_data.append(float(x))
        except Exception as e:
            print(f"Skipped value {e}")

        plt.boxplot([final_data], vert=False, label=["A"])

        plt.title("Boxplot Graph")
        plt.xlabel("Amount")
        plt.grid(True)

        plt.show()


def calculate_data(data):
    '''

    :param data: data set to calculate mmm_r
    :return: calculated data (cal_data)
    '''
    data = [float(i) for i in data]  # Ensure all items are float
    cal_data = {}
    q1_q3 = cal_qs(data)
    cal_data["mean"] = statistics.mean(data)
    cal_data["median"] = statistics.median(data)
    cal_data["mode"] = statistics.mode(data)
    cal_data["range"] = max(data) - min(data)
    cal_data["Q1"] = q1_q3[0]
    cal_data["Q2"] = statistics.median(data)
    cal_data["Q3"] = q1_q3[1]
    cal_data["IQR"] = q1_q3[2]
    cal_data["Outliers"] = cal_Outliers(data, cal_data["Q1"], cal_data["Q3"], cal_data["IQR"])
    cal_data["Standard Deviation"] = statistics.pstdev(data)
    cal_data["Sorted_List"] = sorted(data)
    return cal_data



def main_gui():

    def graph_choice(window):

        def graph_display(parent_window, graph_choice, data):

            def save_report(data,image_name):
                name = simpledialog.askstring("Report Name","What would you like to name your report? ")

                pdf = canvas.Canvas(f"{name}_report.pdf")
                width,height = letter
                pdf.drawCentredString(width/2,height,"Analysis Statistical Report")
                pdf.showPage()
                pdf.save()


            def on_closing(image_name,window):
                if os.path.exists(image_name):
                    os.remove(image_name)
                window.destroy()


            cal_data = calculate_data(data)
            if graph_choice == "boxplot":
                final_data = []
                for x in data:
                    try:
                        final_data.append(float(x))
                    except Exception as e:
                        print(f"Skipped value {e}")

                plt.boxplot([final_data], vert=False, label=["A"])

                plt.title("Boxplot Graph")
                plt.xlabel("Frequency")
                plt.ylabel("Value")
                plt.grid(True)

                with open("number.txt", "r+") as file:
                    number = int(file.read()) + 1
                    file.seek(0)
                    file.write(str(number))

                plt.savefig(f"Graph_{number}.png")

                window = tk.Toplevel(parent_window)
                window.title("Boxplot Graph Results")
                window.attributes("-fullscreen", True)
                window.protocol("WM_DELETE_WINDOW", lambda: on_closing(f"Graph_{number}.png",window) )

                title_label = tk.Label(window, text="Graph Results")
                title_label.pack(padx=20, pady=20)
                title_label.config(font=("Arial", 40))

                image = Image.open(f"Graph_{number}.png")
                img = ImageTk.PhotoImage(image)
                label = tk.Label(window, image=img)
                label.image = img
                label.pack(fill="both", expand=True)

                bottom_frame = tk.Frame(window)
                bottom_frame.pack(pady=20)

                stat_label = tk.Label(bottom_frame, text="Statistical Results:")
                stat_label.pack(pady=20)
                stat_label.config(font=("Arial", 20))

                for x, y in cal_data.items():
                    if x == "Sorted_List":
                        continue
                    label = tk.Label(bottom_frame, text=f"{x.title()} = {y}     ")
                    label.pack(pady=20,fill=tk.Y, side=tk.LEFT)


                save_button = tk.Button(bottom_frame, text="Save Report", command=lambda: save_report(cal_data,f"Graph_{number}.png"))
                save_button.pack(padx=20, pady=20)

            elif graph_choice == "histogram":
                plt.clf()
                final_data = []
                for x in data:
                    try:
                        final_data.append(float(x))
                    except Exception as e:
                        print(f"Skipped value {e}")

                plt.hist(final_data, label=["A"])

                plt.title("Histogram Graph")
                plt.xlabel("Value")
                plt.ylabel("Frequency")
                plt.grid(True)

                with open("number.txt", "r+") as file:
                    number = int(file.read()) + 1
                    file.seek(0)
                    file.write(str(number))

                plt.savefig(f"Graph_{number}.png")

                window = tk.Toplevel(parent_window)
                window.title("Histogram Graph Results")
                window.attributes("-fullscreen", True)
                window.protocol("WM_DELETE_WINDOW", lambda: on_closing(f"Graph_{number}.png", window))

                title_label = tk.Label(window, text="Graph Results")
                title_label.pack(padx=20, pady=20)
                title_label.config(font=("Arial", 40))

                image = Image.open(f"Graph_{number}.png")
                img = ImageTk.PhotoImage(image)
                label = tk.Label(window, image=img)
                label.image = img
                label.pack(fill="both", expand=True)

                bottom_frame = tk.Frame(window)
                bottom_frame.pack(pady=20)

                stat_label = tk.Label(bottom_frame, text="Statistical Results:")
                stat_label.pack(pady=20)
                stat_label.config(font=("Arial", 20))

                for x, y in cal_data.items():
                    if x == "Sorted_List":
                        continue
                    label = tk.Label(bottom_frame, text=f"{x.title()} = {y}     ")
                    label.pack(pady=20, fill=tk.Y, side=tk.LEFT)

                save_button = tk.Button(bottom_frame, text="Save Report",
                                        command=lambda: save_report(cal_data, f"Graph_{number}.png"))
                save_button.pack(padx=20, pady=20)


        choice = middle_entry.get()
        data = []

        if choice.isdigit() or isfloat(choice):
            data.append(float(choice))

        elif "," in choice:
            list1 = choice.split(",")
            for i in list1:
                data.append(i)

        elif choice[0].isdigit() or isfloat(choice[0]):
            numbers_list = []

            for x in choice:

                if x.isdigit():
                    numbers_list.append(x)

                elif x == ".":
                    numbers_list.append(x)

                # Checks to see if the user has entered a times
                elif x == "x":
                    numbers = str(numbers_list)
                    numbers = numbers.replace(",", "")
                    numbers = numbers.replace(" ", "")
                    numbers = numbers.replace("[", "")
                    numbers = numbers.replace("]", "")
                    numbers = numbers.replace("'", "")

                    # Checks if numbers is a digit
                    if numbers.isdigit() or isfloat(numbers):
                        index = choice.index(x)
                        second_numbers = choice[index + 1:]

                        # Makes sure the rest of the numbers are digits
                        if second_numbers.isdigit():
                            numbers = numbers + " "
                            second_numbers = int(second_numbers)
                            product = numbers * second_numbers
                            product = product.split(" ")

                            for x in product:
                                if isfloat(x):
                                    data.append(float(x))
                                else:
                                    break

                        else:
                            messagebox.showerror("Error", "Please enter a number")
                            print("Second Number(s) is not a digit")
                    else:
                        messagebox.showerror("Error", "Please enter a number")
                        print("Please enter a number")
                else:
                    messagebox.showerror("Error", "Please enter a number")
                    print("Please enter a number or a product")

        if hasattr(window, "lower_frame") and window.lower_frame.winfo_exists():
            window.lower_frame.destroy()

        if hasattr(window, "lower_frame") and window.lower_frame.winfo_exists():
            window.lower_frame.destroy()

        window.lower_frame = tk.Frame(window)
        window.lower_frame.pack(pady=30)

        graph_title = tk.Label(window.lower_frame, text="Choose a Graph:")
        graph_title.pack()
        box_plot = tk.Button(window.lower_frame, text="Boxplot", command=lambda: graph_display(window, "boxplot", data))
        box_plot.pack()
        histogram_plot = tk.Button(window.lower_frame, text="Histogram", command=lambda: graph_display(window, "histogram", data))
        histogram_plot.pack()

        plt.close()

    window = tk.Tk()
    window.title("Calculator")
    window.geometry("400x570")

    title_frame = tk.Frame(window)
    title_frame.pack(pady=20)
    title_label = tk.Label(title_frame, text="Calculator")
    title_label.pack(pady=20)
    title_label.config(font=("Arial", 40))

    middle_frame = tk.Frame(window)
    middle_frame.pack(pady=20)
    middle_label = tk.Label(middle_frame, text="Enter Data:")
    middle_label.pack(pady=20)
    middle_entry = tk.Entry(middle_frame)
    middle_entry.pack(pady=20)

    submit_button = tk.Button(middle_frame,text="Submit",command=lambda: graph_choice(window))
    submit_button.pack(pady=20)


    window.mainloop()


if __name__ == '__main__':
    main_gui()