import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import h5py

root = '/home/as1530/'

step = 20

def plot(y0):
    with h5py.File(f'{root}flds.tot.{step:05d}', 'r') as f:
        take_slice = (slice(None), y0, slice(None))
        density = np.sum([f[f'dens{i}'][take_slice] for i in [1, 2, 3, 7, 8, 9]], 0)
        bx = f['bx'][take_slice]
        bz = f['bz'][take_slice]
        x = f['xx'][take_slice][0]
        z = f['zz'][take_slice][:, 0]
    
    xmin, xmax, zmin, zmax = x.min(), x.max(), z.min(), z.max()
    plt.figure(figsize=(10, 10), dpi=100)
    plt.imshow(density,
        cmap='turbo', norm=mpl.colors.Normalize(0, 20),
        origin='lower', extent=(xmin, xmax, zmin, zmax))
    
    plt.streamplot(x, z, bx, bz,
        density=2, color='w',
        linewidth=0.1, arrowsize=1, arrowstyle='->')


    plt.xlabel('x [cells]')
    plt.ylabel('z [cells]')
    plt.xlim(xmin, xmax)
    plt.ylim(zmin, zmax)

    plt.savefig(f'fig{y0}.png')
    plt.close()
    
for y in range(0, 50):
    nm = y*10
    plot(nm)
    print(nm)

# ffmpeg -r 10 -i folder/fig%d.png -c:v libx264 -pix_fmt yuv420p folder.mp4
