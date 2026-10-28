"""Cena 3D de teste para o canal de finanças: cartão de crédito girando e moedas caindo.
Uso: blender -b -P blender/cena_cartao.py -- --saida saida/blender/cartao_ --frames 1-1 --res 540 --amostras 48
Renderiza com Cycles (CPU aqui; no PC do Tiago, GPU NVIDIA com OptiX).
"""
import bpy, math, sys, random, argparse

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument('--saida', default='saida/blender/cartao_')
ap.add_argument('--frames', default='1-90')
ap.add_argument('--res', type=int, default=1080)        # largura; altura = 16:9 vertical
ap.add_argument('--amostras', type=int, default=64)
ap.add_argument('--gpu', action='store_true')
a = ap.parse_args(argv)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
f0, f1 = (int(x) for x in a.frames.split('-'))
sc.frame_start, sc.frame_end = f0, f1
sc.render.fps = 30
sc.render.resolution_x, sc.render.resolution_y = a.res, int(a.res * 16 / 9)
sc.render.engine = 'CYCLES'
sc.cycles.samples = a.amostras
sc.cycles.use_denoising = a.gpu  # o Blender oficial tem denoiser; o do Ubuntu não
if a.gpu:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'
    prefs.get_devices()
    for d in prefs.devices: d.use = True
    sc.cycles.device = 'GPU'
sc.render.filepath = a.saida
sc.render.image_settings.file_format = 'PNG'
sc.view_settings.view_transform = 'AgX' if 'AgX' in [v.identifier for v in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items] else 'Filmic'

def mat(nome, cor, metal=0.0, rug=0.4, emis=None):
    m = bpy.data.materials.new(nome); m.use_nodes = True
    p = m.node_tree.nodes['Principled BSDF']
    p.inputs['Base Color'].default_value = (*cor, 1)
    p.inputs['Metallic'].default_value = metal
    p.inputs['Roughness'].default_value = rug
    if emis:
        k = 'Emission Color' if 'Emission Color' in p.inputs else 'Emission'
        p.inputs[k].default_value = (*emis, 1)
        p.inputs['Emission Strength'].default_value = 2.0
    return m

# fundo: estúdio verde-escuro com gradiente
w = bpy.data.worlds.new('mundo'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.02, 0.05, 0.035, 1)
w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.35

# chão infinito (curva) para sombra suave
bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, -1.6))
chao = bpy.context.object; chao.data.materials.append(mat('chao', (0.02, 0.06, 0.04), rug=0.35))

# cartão: caixa com bordas arredondadas
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0.6))
c = bpy.context.object; c.scale = (1.71, 0.05, 1.08)
bev = c.modifiers.new('bevel', 'BEVEL'); bev.width = 0.06; bev.segments = 8
bpy.ops.object.shade_smooth()
c.data.materials.append(mat('cartao', (0.55, 0.03, 0.03), metal=0.1, rug=0.22))
# chip dourado
bpy.ops.mesh.primitive_cube_add(size=1, location=(-0.5, -0.03, 0.75))
chip = bpy.context.object; chip.scale = (0.26, 0.02, 0.2)
chip.data.materials.append(mat('chip', (1.0, 0.75, 0.25), metal=1.0, rug=0.2))
chip.parent = c; chip.matrix_parent_inverse = c.matrix_world.inverted()
# faixa clara
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, -0.03, 0.25))
fx = bpy.context.object; fx.scale = (1.5, 0.02, 0.07)
fx.data.materials.append(mat('faixa', (0.98, 0.96, 0.9), rug=0.5))
fx.parent = c; fx.matrix_parent_inverse = c.matrix_world.inverted()
# giro do cartão
c.rotation_euler = (math.radians(8), 0, math.radians(-25))
c.keyframe_insert('rotation_euler', frame=f0)
c.rotation_euler = (math.radians(8), 0, math.radians(-25 + 360))
c.keyframe_insert('rotation_euler', frame=max(f0 + 1, 90))
for fc in c.animation_data.action.fcurves:
    for k in fc.keyframe_points: k.interpolation = 'LINEAR'

# moedas caindo
ouro = mat('ouro', (1.0, 0.72, 0.2), metal=1.0, rug=0.18)
random.seed(4)
for i in range(18):
    x, y = random.uniform(-1.1, 1.1), random.uniform(-0.4, 1.4)
    bpy.ops.mesh.primitive_cylinder_add(radius=0.22, depth=0.05, vertices=48, location=(x, y, 0))
    m = bpy.context.object; m.data.materials.append(ouro)
    bv = m.modifiers.new('b', 'BEVEL'); bv.width = 0.012; bv.segments = 3
    bpy.ops.object.shade_smooth()
    z0, z1 = 3.2 + random.uniform(0, 2), -1.55 + 0.03 * (i % 4)
    t0 = random.randint(0, 55)
    m.rotation_euler = (random.uniform(0, 3), random.uniform(0, 3), 0)
    m.location.z = z0; m.keyframe_insert('location', index=2, frame=f0 + t0)
    m.location.z = z1; m.keyframe_insert('location', index=2, frame=f0 + t0 + 25)
    m.keyframe_insert('rotation_euler', frame=f0 + t0)
    m.rotation_euler = (math.radians(90), 0, random.uniform(0, 6)); m.keyframe_insert('rotation_euler', frame=f0 + t0 + 25)

# luzes de estúdio
def luz(loc, energia, cor=(1, 1, 1), tam=3):
    bpy.ops.object.light_add(type='AREA', location=loc)
    l = bpy.context.object; l.data.energy = energia; l.data.color = cor; l.data.size = tam
    d = l.constraints.new('TRACK_TO'); d.target = c; d.track_axis = 'TRACK_NEGATIVE_Z'; d.up_axis = 'UP_Y'
luz((-3, -4, 4), 350, (1.0, 0.95, 0.88))
luz((4, -2, 2), 180, (0.9, 1.0, 0.95))
luz((0, 4, 3), 600, (0.5, 1.0, 0.65), tam=5)   # contraluz verde

# câmera com profundidade de campo
bpy.ops.object.camera_add(location=(0, -7.5, 0.2))
cam = bpy.context.object; sc.camera = cam
cam.data.lens = 50
tc = cam.constraints.new('TRACK_TO'); tc.target = c; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
cam.data.dof.use_dof = True; cam.data.dof.focus_object = c; cam.data.dof.aperture_fstop = 2.2
cam.location.y = -8.2; cam.keyframe_insert('location', frame=f0)
cam.location.y = -6.8; cam.keyframe_insert('location', frame=max(f0 + 1, 90))

bpy.ops.render.render(animation=True)
