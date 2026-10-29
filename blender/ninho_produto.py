"""Ninho Alto (marca conceito): fotos de produto em 3D, feitas só por código.
Cenas: hero (três pacotes na pedra com grãos), pacote (um pacote, giro para vídeo), graos (macro dos grãos).
Uso: blender -b -P blender/ninho_produto.py -- --cena hero --res 1600 --amostras 96 --saida saida/ninho/hero_
     (ou: python3 blender/ninho_produto.py -- ... com o módulo bpy instalado)
Antes: python3 tools/rotulo_ninho.py  (gera as texturas dos rótulos em saida/ninho/)
No PC do Tiago: acrescente --gpu (OptiX).
"""
import bpy, bmesh, math, sys, os, random, argparse
from mathutils import Vector

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
ap = argparse.ArgumentParser()
ap.add_argument('--cena', default='hero', choices=['hero', 'pacote', 'graos'])
ap.add_argument('--lote', default='reserve')
ap.add_argument('--saida', default='saida/ninho/hero_')
ap.add_argument('--frames', default='1-1')
ap.add_argument('--res', type=int, default=1600)
ap.add_argument('--proporcao', default='16:10')
ap.add_argument('--amostras', type=int, default=96)
ap.add_argument('--gpu', action='store_true')
a = ap.parse_args(argv)
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
random.seed(7)

bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
f0, f1 = (int(x) for x in a.frames.split('-'))
sc.frame_start, sc.frame_end, sc.render.fps = f0, f1, 30
pw, ph = (float(x) for x in a.proporcao.split(':'))
sc.render.resolution_x, sc.render.resolution_y = a.res, int(round(a.res * ph / pw))
sc.render.engine = 'CYCLES'
sc.cycles.samples = a.amostras
sc.cycles.use_denoising = True
try: sc.cycles.denoiser = 'OPENIMAGEDENOISE'
except Exception: pass
if a.gpu:
    prefs = bpy.context.preferences.addons['cycles'].preferences
    prefs.compute_device_type = 'OPTIX'; prefs.get_devices()
    for d in prefs.devices: d.use = True
    sc.cycles.device = 'GPU'
sc.render.filepath = os.path.join(RAIZ, a.saida) if not os.path.isabs(a.saida) else a.saida
sc.render.image_settings.file_format = 'PNG'
vts = [v.identifier for v in bpy.types.ColorManagedViewSettings.bl_rna.properties['view_transform'].enum_items]
sc.view_settings.view_transform = 'AgX' if 'AgX' in vts else 'Filmic'
try: sc.view_settings.look = 'AgX - Medium High Contrast' if 'AgX' in vts else 'Medium High Contrast'
except Exception: pass

LOTES = {'sunrise': (0.55, 0.30, 0.06), 'night': (0.04, 0.07, 0.14), 'reserve': (0.30, 0.035, 0.03)}

def ins(m, nome):
    p = m.node_tree.nodes['Principled BSDF']
    return p.inputs[nome] if nome in p.inputs else None

def principled(nome, cor, rug=0.5, metal=0.0, coat=0.0):
    m = bpy.data.materials.new(nome); m.use_nodes = True
    ins(m, 'Base Color').default_value = (*cor, 1); ins(m, 'Roughness').default_value = rug
    ins(m, 'Metallic').default_value = metal
    c = ins(m, 'Coat Weight') or ins(m, 'Clearcoat')
    if c: c.default_value = coat
    return m

# ---------- materiais ----------
TEX = os.path.join(RAIZ, 'public', 'texturas')
def tem_tex(nome): return os.path.exists(os.path.join(TEX, nome + '_diff.jpg'))

def mat_textura(nome, tex, escala, tinta=(1, 1, 1), rug_mult=1.0, normal=1.0, sat=1.0, chapado=0.0):
    """Material PBR com texturas CC0 da Poly Haven (diff, rough, nor) em public/texturas."""
    m = bpy.data.materials.new(nome); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    p = n['Principled BSDF']
    tc = n.new('ShaderNodeTexCoord'); mp = n.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = escala
    l.new(tc.outputs['Object'], mp.inputs['Vector'])
    def img(sufixo, cor):
        i = n.new('ShaderNodeTexImage'); i.projection = 'BOX'; i.projection_blend = 0.2
        i.image = bpy.data.images.load(os.path.join(TEX, f'{tex}_{sufixo}.jpg'))
        if not cor: i.image.colorspace_settings.name = 'Non-Color'
        l.new(mp.outputs['Vector'], i.inputs['Vector']); return i
    d0 = img('diff', True); hs = n.new('ShaderNodeHueSaturation'); hs.inputs['Saturation'].default_value = sat
    l.new(d0.outputs['Color'], hs.inputs['Color'])
    fl = n.new('ShaderNodeMix'); fl.data_type = 'RGBA'; fl.inputs['Factor'].default_value = chapado; fl.inputs['B'].default_value = (0.5, 0.5, 0.5, 1)
    l.new(hs.outputs['Color'], fl.inputs['A'])
    d = fl; mix = n.new('ShaderNodeMix'); mix.data_type = 'RGBA'; mix.blend_type = 'MULTIPLY'
    mix.inputs['Factor'].default_value = 1.0; mix.inputs['B'].default_value = (*tinta, 1)
    l.new(d.outputs['Result'], mix.inputs['A']); l.new(mix.outputs['Result'], p.inputs['Base Color'])
    rg = img('rough', False); mt = n.new('ShaderNodeMath'); mt.operation = 'MULTIPLY'; mt.inputs[1].default_value = rug_mult
    l.new(rg.outputs['Color'], mt.inputs[0]); l.new(mt.outputs['Value'], p.inputs['Roughness'])
    nm = n.new('ShaderNodeNormalMap'); nm.inputs['Strength'].default_value = normal
    l.new(img('nor', False).outputs['Color'], nm.inputs['Color']); l.new(nm.outputs['Normal'], p.inputs['Normal'])
    return m

def mat_pedra():
    if tem_tex('concrete_floor_01'):
        return mat_textura('pedra', 'concrete_floor_01', (1.8, 1.8, 1.8), tinta=(1.05, 1.04, 1.04), normal=0.6, sat=0.15, chapado=0.25)
    m = bpy.data.materials.new('pedra'); m.use_nodes = True; nt = m.node_tree; n = nt.nodes
    p = n['Principled BSDF']; p.inputs['Roughness'].default_value = 0.62  # sem texturas: pedra procedural
    tc = n.new('ShaderNodeTexCoord'); mp = n.new('ShaderNodeMapping'); mp.inputs['Scale'].default_value = (1.2, 4.0, 1.2)
    nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 3.0; nz.inputs['Detail'].default_value = 12
    rp = n.new('ShaderNodeValToRGB'); rp.color_ramp.elements[0].color = (0.22, 0.20, 0.18, 1); rp.color_ramp.elements[1].color = (0.42, 0.39, 0.35, 1)
    nz2 = n.new('ShaderNodeTexNoise'); nz2.inputs['Scale'].default_value = 60; nz2.inputs['Detail'].default_value = 6
    bump = n.new('ShaderNodeBump'); bump.inputs['Strength'].default_value = 0.12
    l = nt.links
    l.new(tc.outputs['Object'], mp.inputs['Vector']); l.new(mp.outputs['Vector'], nz.inputs['Vector'])
    l.new(nz.outputs['Fac'], rp.inputs['Fac']); l.new(rp.outputs['Color'], p.inputs['Base Color'])
    l.new(tc.outputs['Object'], nz2.inputs['Vector']); l.new(nz2.outputs['Fac'], bump.inputs['Height'])
    l.new(bump.outputs['Normal'], p.inputs['Normal'])
    return m

def mat_pacote(lote):
    """Papel fosco com o rótulo na frente (normal -Y) e a cor do lote no resto."""
    m = bpy.data.materials.new('pacote_' + lote); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    p = n['Principled BSDF']; p.inputs['Roughness'].default_value = 0.58
    sh = ins(m, 'Sheen Weight') or ins(m, 'Sheen')
    if sh: sh.default_value = 0.25
    img = n.new('ShaderNodeTexImage')
    _png = os.path.join(RAIZ, 'saida', 'ninho', f'rotulo_{lote}.png')
    _rep = os.path.join(RAIZ, 'portfolio', 'ninho-alto', 'rotulos', f'rotulo_{lote}.png')  # cópia versionada: o PC não precisa de Python
    img.image = bpy.data.images.load(_png if os.path.exists(_png) else _rep)
    geo = n.new('ShaderNodeNewGeometry'); sep = n.new('ShaderNodeSeparateXYZ')
    lt = n.new('ShaderNodeMath'); lt.operation = 'LESS_THAN'; lt.inputs[1].default_value = -0.35
    mix = n.new('ShaderNodeMix'); mix.data_type = 'RGBA'
    mix.inputs['A'].default_value = (*LOTES[lote], 1)
    l.new(geo.outputs['Normal'], sep.inputs['Vector']); l.new(sep.outputs['Y'], lt.inputs[0])
    l.new(lt.outputs['Value'], mix.inputs['Factor']); l.new(img.outputs['Color'], mix.inputs['B'])
    l.new(mix.outputs['Result'], p.inputs['Base Color'])
    # fibra do papel: ruído fino no relevo e na rugosidade
    nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 900; nz.inputs['Detail'].default_value = 4
    bp = n.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.05
    l.new(nz.outputs['Fac'], bp.inputs['Height']); l.new(bp.outputs['Normal'], p.inputs['Normal'])
    rr = n.new('ShaderNodeMapRange'); rr.inputs['To Min'].default_value = 0.5; rr.inputs['To Max'].default_value = 0.7
    l.new(nz.outputs['Fac'], rr.inputs['Value']); l.new(rr.outputs['Result'], p.inputs['Roughness'])
    return m

# ---------- objetos ----------
def pacote(lote, loc, rot_z=0.0, W=0.62, H=0.92, D=0.24):
    """Pacote stand-up: selado e fino no topo, cheio no meio, fundo com sanfona."""
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.subdivide_edges(bm, edges=bm.edges[:], cuts=30, use_grid_fill=True)
    for v in bm.verts:
        x, y, z = v.co.x, v.co.y, v.co.z + 0.5  # z de 0 a 1
        # espessura: 0 no topo selado, cheio no meio, um pouco menos no fundo
        perfil = (math.sin(min(1.0, (1 - z) / 0.82) * math.pi / 2) ** 0.7) * (0.92 + 0.08 * math.sin(z * math.pi))
        if z > 0.9: perfil *= max(0.03, (1 - z) / 0.1) * 0.2
        bojo = 1 - 0.25 * (2 * x) ** 4
        v.co = Vector((x * W * (1 - 0.04 * z), y * D * max(perfil * bojo, 0.012), z * H))
    me = bpy.data.meshes.new('pacote'); bm.to_mesh(me); bm.free()
    # UV: projeção frontal (x, z) para o rótulo
    uv = me.uv_layers.new(name='UV')
    for poly in me.polygons:
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = ((co.x / (W * 0.96)) + 0.5, co.z / H)
    ob = bpy.data.objects.new('pacote_' + lote, me); bpy.context.collection.objects.link(ob)
    ob.location = loc; ob.rotation_euler = (0, 0, rot_z)
    ss = ob.modifiers.new('suave', 'SUBSURF'); ss.levels = ss.render_levels = 2
    tx = bpy.data.textures.new('amassado', 'CLOUDS'); tx.noise_scale = 0.08
    dp = ob.modifiers.new('amassado', 'DISPLACE'); dp.texture = tx; dp.strength = 0.006
    # vincos de papel: células de Voronoi com bordas vivas, fracas, só para quebrar o "plástico liso"
    vx = bpy.data.textures.new('vincos', 'VORONOI'); vx.noise_scale = 0.11; vx.distance_metric = 'DISTANCE'
    vx.noise_intensity = 1.0; vx.contrast = 1.4
    dv = ob.modifiers.new('vincos', 'DISPLACE'); dv.texture = vx; dv.strength = 0.0045; dv.mid_level = 0.6
    dv.texture_coords = 'LOCAL' 
    for poly in me.polygons: poly.use_smooth = True
    ob.data.materials.append(mat_pacote(lote))
    return ob

_grao_me = None
def mat_grao():
    """Grão torrado: cor varia de grão para grão (Object Info › Random), superfície celular fosca
    e a película clara (silverskin) dentro da fenda, lida do atributo 'fenda' da malha."""
    m = bpy.data.materials.new('grao'); m.use_nodes = True; nt = m.node_tree; n = nt.nodes; l = nt.links
    p = n['Principled BSDF']
    oi = n.new('ShaderNodeObjectInfo'); rp = n.new('ShaderNodeValToRGB')
    rp.color_ramp.elements[0].color = (0.072, 0.034, 0.015, 1); rp.color_ramp.elements[1].color = (0.020, 0.009, 0.005, 1)
    l.new(oi.outputs['Random'], rp.inputs['Fac'])
    vo = n.new('ShaderNodeTexVoronoi'); vo.inputs['Scale'].default_value = 260
    nz = n.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 60; nz.inputs['Detail'].default_value = 6
    mx = n.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs['Factor'].default_value = 0.3
    l.new(rp.outputs['Color'], mx.inputs['A']); l.new(nz.outputs['Color'], mx.inputs['B'])
    at = n.new('ShaderNodeAttribute'); at.attribute_name = 'fenda'
    pele = n.new('ShaderNodeMix'); pele.data_type = 'RGBA'; pele.inputs['B'].default_value = (0.32, 0.20, 0.11, 1)
    l.new(at.outputs['Fac'], pele.inputs['Factor']); l.new(mx.outputs['Result'], pele.inputs['A'])
    l.new(pele.outputs['Result'], p.inputs['Base Color'])
    rr = n.new('ShaderNodeMapRange'); rr.inputs['To Min'].default_value = 0.48; rr.inputs['To Max'].default_value = 0.72
    l.new(nz.outputs['Fac'], rr.inputs['Value']); l.new(rr.outputs['Result'], p.inputs['Roughness'])
    bp = n.new('ShaderNodeBump'); bp.inputs['Strength'].default_value = 0.5; bp.inputs['Distance'].default_value = 0.0015
    l.new(vo.outputs['Distance'], bp.inputs['Height']); l.new(bp.outputs['Normal'], p.inputs['Normal'])
    c = ins(m, 'Coat Weight') or ins(m, 'Clearcoat')
    if c: c.default_value = 0.05
    return m

def grao(loc, esc=1.0):
    global _grao_me
    if _grao_me is None:
        rng = random.Random(11)
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=64, v_segments=40, radius=1.0)
        fenda = {}
        for v in bm.verts:
            x, y, z = v.co
            if z > 0: z *= 0.34  # lado chato
            s = abs(x - 0.12 * math.sin(y * 2.6))  # S da fenda
            w = 0.075
            f = 0.0
            if z > 0.05 and s < w and abs(y) < 0.9:
                f = (1 - s / w) ** 1.2
                z -= 0.95 * f * z  # fenda estreita e funda
            # irregularidade: nenhum grão é um ovo perfeito
            k = 1 + 0.035 * math.sin(3.1 * y + 1.3) * math.cos(2.3 * x) + rng.uniform(-0.004, 0.004)
            v.co = Vector((x * 0.019 * k, y * 0.029 * k, z * 0.017 + 0.006))
            fenda[v.index] = f
        me = bpy.data.meshes.new('grao'); bm.to_mesh(me); bm.free()
        cor = me.color_attributes.new('fenda', 'FLOAT_COLOR', 'POINT')
        for vi, f in fenda.items(): cor.data[vi].color = (f, f, f, 1)
        for p in me.polygons: p.use_smooth = True
        me.materials.append(mat_grao()); _grao_me = me
    ob = bpy.data.objects.new('grao', _grao_me); bpy.context.collection.objects.link(ob)
    ob.location = loc; ob.scale = (esc * random.uniform(.88, 1.1), esc * random.uniform(.9, 1.12), esc * random.uniform(.92, 1.08))
    ob.rotation_euler = (random.uniform(-.25, .25) + (math.pi if random.random() < .45 else 0), random.uniform(-.2, .2), random.uniform(0, 2 * math.pi))
    return ob

def chao_e_parede(cor_parede=(0.30, 0.285, 0.265)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0.2, -0.04)); laje = bpy.context.object
    laje.scale = (3.4, 1.6, 0.08); laje.data.materials.append(mat_pedra())
    bv = laje.modifiers.new('b', 'BEVEL'); bv.width = 0.01; bv.segments = 3
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 4.0, 0), rotation=(math.pi / 2, 0, 0))
    parede = mat_textura('parede', 'grey_plaster', (0.8, 0.8, 0.8), tinta=tuple(c * 2.0 for c in cor_parede), normal=0.5, sat=0.2, chapado=0.55) if tem_tex('grey_plaster') else principled('parede', cor_parede, rug=0.9)
    bpy.context.object.data.materials.append(parede)
    bpy.ops.mesh.primitive_plane_add(size=30, location=(0, 0, -0.081))
    bpy.context.object.data.materials.append(principled('piso', (0.36, 0.33, 0.30), rug=0.8))

def luzes(forca=1.0):
    w = bpy.data.worlds.new('mundo'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.86, 0.84, 0.80, 1)
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.08
    hdr = os.path.join(TEX, 'art_studio_1k.hdr')
    if os.path.exists(hdr):  # estúdio com janelas: reflexos reais no papel e nos grãos
        env = w.node_tree.nodes.new('ShaderNodeTexEnvironment'); env.image = bpy.data.images.load(hdr)
        w.node_tree.links.new(env.outputs['Color'], w.node_tree.nodes['Background'].inputs['Color'])
        w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.12
    def area(nome, loc, rot, tam, energia, cor=(1, 0.96, 0.9)):
        d = bpy.data.lights.new(nome, 'AREA'); d.size = tam; d.energy = energia * forca; d.color = cor
        o = bpy.data.objects.new(nome, d); bpy.context.collection.objects.link(o); o.location = loc; o.rotation_euler = rot
    area('janela', (-3.2, -1.2, 2.6), (math.radians(55), 0, math.radians(-65)), 2.4, 280)   # chave: janela à esquerda
    area('rebate', (3.0, -2.5, 1.0), (math.radians(75), 0, math.radians(50)), 3.0, 60, (0.9, 0.95, 1))
    area('recorte', (1.2, 2.6, 2.2), (math.radians(-60), 0, math.radians(160)), 1.2, 160)

def camera(loc, alvo, lente=70, foco=None, f=2.8):
    c = bpy.data.cameras.new('cam'); c.lens = lente
    o = bpy.data.objects.new('cam', c); bpy.context.collection.objects.link(o); sc.camera = o
    o.location = loc
    d = Vector(alvo) - Vector(loc); o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
    c.dof.use_dof = True; c.dof.aperture_fstop = f; c.dof.focus_distance = foco or d.length
    return o

# ---------- cenas ----------
if a.cena == 'hero':
    chao_e_parede(); luzes()
    pacote('sunrise', (-0.78, 0.35, 0), math.radians(14))
    pacote('night', (0.80, 0.42, 0), math.radians(-12))
    pacote('reserve', (0.0, 0.0, 0), math.radians(3))
    for _ in range(420):  # monte derramado na frente do Reserve
        r = abs(random.gauss(0, 0.32)); t = random.uniform(0, 2 * math.pi)
        x, y = 0.45 + r * math.cos(t) * 1.6, -0.55 + r * math.sin(t) * 0.5
        z = max(0.0, 0.05 - r * 0.12) * random.random()
        grao((x, y, z))
    camera((0.55, -4.1, 0.85), (0.1, 0.1, 0.38), lente=60, f=3.2)
elif a.cena == 'pacote':
    chao_e_parede((0.74, 0.72, 0.68)); luzes()
    p = pacote(a.lote, (0, 0.2, 0))
    p.rotation_euler = (0, 0, math.radians(-35)); p.keyframe_insert('rotation_euler', frame=f0)
    p.rotation_euler = (0, 0, math.radians(35)); p.keyframe_insert('rotation_euler', frame=max(f1, f0 + 1))
    for _ in range(140):
        grao((random.gauss(0.35, 0.3), random.gauss(-0.35, 0.12), 0.0))
    camera((0.0, -3.0, 0.75), (0, 0.2, 0.45), lente=60, f=3.2)
else:  # graos
    chao_e_parede(); luzes(0.8)
    pts = []  # uma camada de grãos sem encostar (sorteio com distância mínima)
    while len(pts) < 420:
        p = (random.uniform(-0.5, 0.5), random.uniform(-0.3, 0.5))
        if all((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 > 0.034 ** 2 for q in pts): pts.append(p)
    for x, y in pts: grao((x, y, 0.0), esc=random.uniform(0.9, 1.1))
    camera((0.05, -0.62, 0.30), (0.0, 0.06, 0.0), lente=85, f=4.0)

bpy.ops.render.render(animation=(f1 > f0), write_still=(f1 == f0))
print('ok', sc.render.filepath)
