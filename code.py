import numpy as np
from PIL import Image


class Node: 


    def __init__(self, x, y, size, depth=0, maxdepth=9):
        self.x = x
        self.y = y
        self.size = size
        self.depth = depth
        self.maxdepth = maxdepth
        self.children = []
        self.color = None

    def split(self, img, threshold=25):


        block = img[int(self.y):int(self.y+self.size), int(self.x):int(self.x+self.size)]
        self.color = np.mean(block.reshape(-1,3), axis=0)
        var = np.var(block.reshape(-1,3), axis=0).mean()

        if self.depth >= self.maxdepth or var < threshold or self.size <= 2:
            return

        half = self.size // 2
        for dx in [0, half]:
            for dy in [0, half]:
                child = Node(self.x + dx, self.y + dy, half, self.depth + 1, self.maxdepth)
                child.split(img, threshold)
                self.children.append(child)

def draw(node, canvas):
    if not node.children: 
        x, y, s = int(node.x), int(node.y), int(node.size)
        canvas[y:y+s, x:x+s] = node.color

        

    else:
        for child in node.children:
            draw(child, canvas)

print("Your image is being reduced.")
print("Its gonna take some time T-T")

img_path = "city.jpg"
scale = 1.5
img = Image.open(img_path).convert("RGB")
w, h = img.size
arr = np.array(img, dtype=np.float32)
size = 1 << (max(w, h) - 1).bit_length()
canvas = np.zeros((size, size, 3), dtype=np.float32)
canvas[:h, :w] = arr
root = Node(0, 0, size, maxdepth=10)
root.split(canvas, threshold=25)



compressed = np.zeros_like(canvas)
draw(root, compressed)
compressed = compressed[:h, :w]
block = size // (2 ** root.maxdepth)
neww = w//block
newh = h//block

result = Image.fromarray(compressed.astype(np.uint8)).resize(
    (int(neww * scale), int(newh * scale)), Image.NEAREST
)
result.save("newimage.jpg")
print("newimage.jpg saved with size", int(neww * scale), "x", int(newh * scale))
