############################################################################################
# Auther : Harnish Shah
# EmailID: harnishhshah@gmail.com

#############################################################################################
import os
import tkinter as tk
from tkinter import *
from tkinter import filedialog

import cv2
import easyocr
import matplotlib.pyplot as plt
from PIL import Image, ImageTk

window = Tk()
lbl = Label(window)
lbl.pack()

window.title("Harnish: Text Detection Script")
window.geometry('1100x700')
file_name = None


class Detect():
    """
    Class for detecting text
    """

    def recognize_text(self, img_path):
        '''
        loads an image and recognizes text.
        '''

        reader = easyocr.Reader(['en'])
        return reader.readtext(img_path, ycenter_ths=5.0)

    def run(self):
        """
        It will run the script
        Run loaded input image and text from the image will be detected
        """
        try:
            obj = T.get('1.0', 'end-1c')
            print("## obj after click on run ##", obj)

            # open file in read mode
            with open('tmp.txt', 'r') as f:

                img_name = cv2.imread(f.read())
                # print("## image path ###", img_name)

                img = cv2.cvtColor(img_name, cv2.COLOR_BGR2RGB)
                print(img.shape[0], img.shape[1])
                if img.shape[0] < 600:
                    dpi = 10
                    # dpi =80
                    fig_width, fig_height = int(img.shape[0] / dpi), int(img.shape[1] / dpi)
                    print(fig_height, fig_width)
                    plt.figure()
                    f, self.axarr = plt.subplots(1, 2, figsize=(fig_width, fig_height))
                    self.axarr[0].imshow(img)
                else:
                    dpi = 80
                    fig_width, fig_height = int(img.shape[0] / dpi), int(img.shape[1] / dpi)
                    plt.figure()
                    f, self.axarr = plt.subplots(1, 2, figsize=(fig_width, fig_height))
                    self.axarr[0].imshow(img)

                with open('tmp.txt', 'r') as f:
                    # recognize text
                    image = f.read()
                    self.result = self.recognize_text(image)
                    print("## result ##", self.result)

                    self.final_text = ''
                    # if OCR prob is over 0.5, overlay bounding box and text
                    for (bbox, text1, prob) in self.result:
                        if prob >= 0.5:
                            # display
                            print(f'Detected text: {text1} (Probability: {prob:.2f})')

                            # get top-left and bottom-right bbox vertices
                            (top_left, top_right, bottom_right, bottom_left) = bbox
                            self.top_left = (int(top_left[0]), int(top_left[1]))
                            self.bottom_right = (int(bottom_right[0]), int(bottom_right[1]))

                            print("## obj ##", obj)
                            print("## text: ", text1)

                            if obj.lower() in text1.lower():
                                # index = obj.find(text1)
                                # print(" ## Matched2 at ##:-", index)
                                print("plot1", self.top_left)
                                print("plot2", self.bottom_right)

                                # create a rectangle for bbox display
                                cv2.rectangle(img=img, pt1=self.top_left, pt2=self.bottom_right, color=(0, 255, 0),
                                              thickness=10)

                                # put recognized text
                                cv2.putText(img=img, text=text1, org=(self.top_left[0], self.top_left[1] - 10),
                                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                            fontScale=2, color=(255, 0, 0), thickness=2)

                                self.axarr[1].imshow(img)
                                with open('tmp.txt', 'r') as f:
                                    plt.savefig(f'{f.read()}_overlay.jpg', bbox_inches='tight')

                            # if img.shape[0] < 600:
                            #     # create a rectangle for bbox display
                            #     cv2.rectangle(img=img, pt1=self.top_left, pt2=self.bottom_right, color=(255, 0, 0), thickness=5)
                            #
                            #     # put recognized text
                            #     cv2.putText(img=img, text=text, org=(self.top_left[0], self.top_left[1] - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            #                 fontScale=0.5, color=(255, 0, 0), thickness=1)
                            # else:
                            #     # create a rectangle for bbox display
                            #     cv2.rectangle(img=img, pt1=self.top_left, pt2=self.bottom_right, color=(255, 0, 0), thickness=10)
                            #
                            #     # put recognized text
                            #     cv2.putText(img=img, text=text, org=(self.top_left[0],self.top_left[1] - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            #                 fontScale=2, color=(255, 0, 0), thickness=2)

                            # obj = T.get('1.0', 'end-1c')
                            # print("## obj ##", obj)
                            # if obj == text:
                            #     print(" ## Matched2 ##", obj.Text)
                            #     # create a rectangle for bbox display
                            #     cv2.rectangle(img=img, pt1=self.top_left, pt2=self.bottom_right, color=(0, 255, 0), thickness=10)
                            #
                            #     # put recognized text
                            #     cv2.putText(img=img, text=text, org=(self.top_left[0], self.top_left[1] - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            #                 fontScale=2, color=(255, 255, 0), thickness=2)

                            # show and save image
                            self.axarr[1].imshow(img)
                            with open('tmp.txt', 'r') as f:
                                plt.savefig(f'{f.read()}_overlay.jpg', bbox_inches='tight')
                                self.final_text += text1 + ' '

                    print("Final Text :", self.final_text)
                    f = open("write.txt", "w")
                    f.write(self.final_text)


        except FileNotFoundError as e:
            print(e, "file not found")

        f = open("write.txt", "r")
        output = f.readlines()
        print("## Output ##", output)

        try:
            # open file in read mode
            with open('tmp.txt', 'r') as f:
                make = f.read() + '_overlay.jpg'
                img = Image.open(make)
                img.thumbnail((1000, 1000))
                img = ImageTk.PhotoImage(img)
                lbl.configure(image=img)
                lbl.image = img

        except FileNotFoundError as e:
            print(e, "file not found")

    def show_image(self):
        file = filedialog.askopenfilename(initialdir=os.getcwd(), title='Select Image File',
                                          filetypes=(('JPG File', '*jpg'), ('All Files', '*.*')))
        # run(file)
        img = Image.open(file)
        img.thumbnail((500, 500))
        img = ImageTk.PhotoImage(img)
        lbl.configure(image=img)
        lbl.image = img

        file1 = file.split('/')
        print("#####", list(file1))
        file_name = file1[-1]
        print("### file name:", file_name)

        try:
            # open file in write mode
            with open('tmp.txt', 'w') as f:
                f.write(file_name)

        except FileNotFoundError as e:
            pass

    # def search(self):
    #     """
    #
    #     """
    #     text.delete('1.0', END)
    #     f = open("write.txt", "r")
    #     output = f.readlines()
    #     text.insert('1.0', output[0])

    # def find(self):
    #     """
    #
    #     """
    #     # # open file in read mode
    #     # with open('tmp.txt', 'r') as f:
    #     #     img_name = cv2.imread(f.read())
    #     #     img = cv2.cvtColor(img_name, cv2.COLOR_BGR2RGB)
    #     #
    #     #     obj = T.get('1.0', 'end-1c')
    #     #     print("## obj ##", obj)
    #     #     print("## text: ", text.get('1.0','end-1c'))
    #     #     if str(obj) in str(text.get('1.0','end-1c')):
    #     #         print(" ## Matched2 ##", self.result)
    #     #         # create a rectangle for bbox display
    #     #         cv2.rectangle(img=img, pt1=self.top_left, pt2=self.bottom_right, color=(0, 255, 0), thickness=10)
    #     #
    #     #         # # put recognized text
    #     #         # cv2.putText(img=img, text=text, org=(self.top_left[0], self.top_left[1] - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
    #     #         #             fontScale=2, color=(255, 255, 0), thickness=2)
    #     #
    #     #         self.axarr[1].imshow(img)
    #     #         with open('tmp.txt', 'r') as f:
    #     #             plt.savefig(f'{f.read()}_overlay.jpg', bbox_inches='tight')
    #
    #
    #
    #
    #     # remove tag 'found' from index 1 to END
    #     text.tag_remove('found', '1.0', END)
    #
    #     # returns to widget currently in focus
    #     s = T.get('1.0', 'end-1c')
    #     if s:
    #         idx = '1.0'
    #         while 1:
    #             # searches for desried string from index 1
    #             idx = text.search(s, idx, nocase=1,
    #                               stopindex=END)
    #             if not idx: break
    #
    #             # last index sum of current index and
    #             # length of text
    #             lastidx = '%s+%dc' % (idx, len(s))
    #
    #             # overwrite 'Found' at idx
    #             text.tag_add('found', idx, lastidx)
    #             idx = lastidx
    #
    #         # mark located string as red
    #         text.tag_config('found', foreground='red', font=('arial', 9, 'bold'))
    #     T.focus_set()


if __name__ == "__main__":
    obj = Detect()
    btn = Button(window, text="Run", bg="black", fg="white", command=obj.run, height=2, width=10)
    btn.place(x=500, y=600)

    btn = Button(window, text="Browse", bg="black", fg="white", command=obj.show_image, height=2, width=10)
    btn.place(x=300, y=600)

    btn = Button(window, text="Exit", bg="black", fg="white", command=lambda: exit(), height=2, width=10)
    btn.place(x=700, y=600)

    # btn = Button(window, text="Add", bg="black", fg="white", command=obj.search, height=2, width=10)
    # btn.place(x=600, y=600)

    label = tk.Label(window, text='Text to find:')
    label.place(relx=0.25, rely=0.6, anchor='center')

    T = tk.Text(window, height=2, width=52)
    T.place(relx=0.5, rely=0.6, anchor='center')

    # butt = Button(window, text='Find', height=2, width=10, command=obj.find)
    # butt.place(x=800, y=500)
    # butt.config(command=obj.find)

    # # text box in root window
    # text = Text(window, height=12, width=52)
    # text.place(relx=0.5, rely=0.67, anchor='center')

    window.mainloop()
