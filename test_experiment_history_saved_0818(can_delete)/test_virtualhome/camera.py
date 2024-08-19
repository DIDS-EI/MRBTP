


from mabtpg.envs.virtualhome.envs.vh_env import VHEnvTest


env = VHEnvTest()
env.load_scenario(0) # 18
comm = env.comm

# Get graph
s, graph = comm.environment_graph()

# Get the fridge node
fridge_node = [node for node in graph['nodes'] if node['class_name'] == 'fridge'][0]

# Open it
fridge_node['states'] = ['OPEN']

# update the environment
comm.expand_scene(graph)



s, cam_count = comm.camera_count()

# Add a camera at the specified rotation and position
comm.add_camera(position=[-3, 2, -5], rotation=[10, 15, 0])

# View camera from different modes
modes = ['normal']
images = []
for mode in modes:
    s, im = comm.camera_image([cam_count], mode=mode)
    images.append(im[0])




# create a new node
new_node = {
    'id': 1000,
    'class_name': 'salmon',
    'states': []
}
# Add an edge
new_edge = {'from_id': 1000, 'to_id': fridge_node['id'], 'relation_type': 'INSIDE'}
graph['nodes'].append(new_node)
graph['edges'].append(new_edge)

# update the environment
comm.expand_scene(graph)


for mode in modes:
    s, im = comm.camera_image([cam_count], mode=mode)
    images.append(im[0])







import matplotlib.pyplot as plt
import matplotlib.image as mpimg


def display_images_vertically(images, titles=None):
    """
    自动竖向排列和显示多张图片

    参数:
    images (list of np.array): 图片列表，每个元素是一个NumPy数组，表示一张图片
    titles (list of str): 每张图片的标题（可选）
    """
    rows = len(images)
    cols = 1

    fig, axes = plt.subplots(rows, cols, figsize=(5, 5 * rows))
    axes = axes.flatten() if rows > 1 else [axes]

    for i, img in enumerate(images):
        # 转换颜色通道顺序从 BGR 到 RGB
        if img.shape[2] == 3:
            img = img[..., ::-1]
        axes[i].imshow(img)
        axes[i].axis('off')  # 不显示坐标轴
        if titles is not None and i < len(titles):
            axes[i].set_title(titles[i])


    plt.tight_layout()
    plt.show()

display_images_vertically(images)
