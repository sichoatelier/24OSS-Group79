import tkinter as tk
from main_gui import show_main_gui
from skin_tone_test.skin_tone_gui import show_skin_tone_test
from facial_asymmetry_test.facial_asymmetry_gui import show_facial_asymmetry_test
from art_recommendation_test.art_recommendation_gui import show_art_recommendation_test

def main():
    root = tk.Tk()
    root.title("얼굴로 하는 테스트")
    root.geometry("640x480")
    
    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)
    
    def return_to_main():
        show_main_gui(main_frame, show_skin_tone, show_facial_asymmetry, show_art_recommendation)

    def show_skin_tone():
        show_skin_tone_test(main_frame, return_to_main)

    def show_facial_asymmetry():
        show_facial_asymmetry_test(main_frame, return_to_main)

    def show_art_recommendation():
        show_art_recommendation_test(main_frame, return_to_main)
    
    return_to_main()

    root.mainloop()

if __name__ == "__main__":
    main()
