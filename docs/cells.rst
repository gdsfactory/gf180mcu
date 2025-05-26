

Here are the parametric cells available in the PDK

.. note::
   If you were previously using the ``gf180`` package, it has been renamed to ``gf180mcu``. The original ``gf180`` package is now deprecated.
   See the :doc:`migration` guide for more information.


Cells
=============================


alter_interdig
----------------------------------------------------

.. autofunction:: gf180mcu.alter_interdig

.. plot::
  :include-source:

  import gf180mcu

  c = gf180mcu.alter_interdig(l_gate=0.15, inter_sd_l=0.15, sd_l=0.36, nf=1, pat='', pc_x=0.1, pc_spacing=0.1, label=0, nl=1, patt_label=0)
  c.plot()



cap_mos
----------------------------------------------------

.. autofunction:: gf180mcu.cap_mos

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.cap_mos(type='cap_nmos', lc=0.1, wc=0.1, volt='3.3V', deepnwell=0, pcmpgr=0, label=0, g_label='', sd_label='')
  c.plot()



cap_mos_inst
----------------------------------------------------

.. autofunction:: gf180mcu.cap_mos_inst

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.cap_mos_inst(lc=0.1, wc=0.1, cmp_w=0.1, con_w=0.1, pl_l=0.1, cmp_ext=0.1, pl_ext=0.1, implant_layer=(32, 0), implant_enc=(0.1, 0.1), label=0, g_label='')
  c.plot()



diode_dw2ps
----------------------------------------------------

.. autofunction:: gf180mcu.diode_dw2ps

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.diode_dw2ps(la=0.1, wa=0.1, cw=0.1, volt='3.3V', pcmpgr=0, label=0, p_label='', n_label='')
  c.plot()



diode_nd2ps
----------------------------------------------------

.. autofunction:: gf180mcu.diode_nd2ps

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.diode_nd2ps(la=0.1, wa=0.1, cw=0.1, volt='3.3V', deepnwell=0, pcmpgr=0, label=0, p_label='', n_label='')
  c.plot()



diode_nw2ps
----------------------------------------------------

.. autofunction:: gf180mcu.diode_nw2ps

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.diode_nw2ps(la=0.1, wa=0.1, cw=0.1, volt='3.3V', label=0, p_label='', n_label='')
  c.plot()



diode_pd2nw
----------------------------------------------------

.. autofunction:: gf180mcu.diode_pd2nw

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.diode_pd2nw(la=0.1, wa=0.1, cw=0.1, volt='3.3V', deepnwell=0, pcmpgr=0, label=0, p_label='', n_label='')
  c.plot()



diode_pw2dw
----------------------------------------------------

.. autofunction:: gf180mcu.diode_pw2dw

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.diode_pw2dw(la=0.1, wa=0.1, cw=0.1, volt='3.3V', pcmpgr=0, label=0, p_label='', n_label='')
  c.plot()



interdigit
----------------------------------------------------

.. autofunction:: gf180mcu.interdigit

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.interdigit(l_gate=0.15, inter_sd_l=0.23, sd_l=0.15, nf=1, gate_con_pos='top', pc_x=0.1, pc_spacing=0.1, label=0, patt_label=0)
  c.plot()



labels_gen
----------------------------------------------------

.. autofunction:: gf180mcu.labels_gen

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.labels_gen(label_str='', position=(0.1, 0.1), layer=(34, 10), label=0, label_valid_len=1, index=0)
  c.plot()



nfet
----------------------------------------------------

.. autofunction:: gf180mcu.nfet

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.nfet(l_gate=0.28, w_gate=0.22, sd_con_col=1, inter_sd_l=0.24, nf=1, grw=0.22, volt='3.3V', bulk='None', con_bet_fin=1, gate_con_pos='alternating', interdig=0, patt='', deepnwell=0, pcmpgr=0, label=0, sub_label='', patt_label=0)
  c.plot()



nfet_06v0_nvt
----------------------------------------------------

.. autofunction:: gf180mcu.nfet_06v0_nvt

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.nfet_06v0_nvt(l_gate=1.8, w_gate=0.8, sd_con_col=1, inter_sd_l=0.24, nf=1, grw=0.22, bulk='None', con_bet_fin=1, gate_con_pos='alternating', interdig=0, patt='', label=0, sub_label='', patt_label=0)
  c.plot()



nfet_deep_nwell
----------------------------------------------------

.. autofunction:: gf180mcu.nfet_deep_nwell

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.nfet_deep_nwell(deepnwell=0, pcmpgr=0, inst_size=(0.1, 0.1), inst_xmin=0.1, inst_ymin=0.1, grw=0.36)
  c.plot()



nplus_res
----------------------------------------------------

.. autofunction:: gf180mcu.nplus_res

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.nplus_res(l_res=0.1, w_res=0.1, res_type='nplus_s', sub=0, deepnwell=0, pcmpgr=0, label=0, r0_label='', r1_label='', sub_label='')
  c.plot()



npolyf_res
----------------------------------------------------

.. autofunction:: gf180mcu.npolyf_res

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.npolyf_res(l_res=0.1, w_res=0.1, res_type='npolyf_s', deepnwell=0, pcmpgr=0, label=0, r0_label='', r1_label='', sub_label='')
  c.plot()



pcmpgr_gen
----------------------------------------------------

.. autofunction:: gf180mcu.pcmpgr_gen

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.pcmpgr_gen(grw=0.36)
  c.plot()



pfet
----------------------------------------------------

.. autofunction:: gf180mcu.pfet

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.pfet(l_gate=0.28, w_gate=0.22, sd_con_col=1, inter_sd_l=0.24, nf=1, grw=0.22, volt='3.3V', bulk='None', con_bet_fin=1, gate_con_pos='alternating', interdig=0, patt='', deepnwell=0, pcmpgr=0, label=0, sub_label='', patt_label=0)
  c.plot()



pfet_deep_nwell
----------------------------------------------------

.. autofunction:: gf180mcu.pfet_deep_nwell

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.pfet_deep_nwell(deepnwell=0, pcmpgr=0, enc_size=(0.1, 0.1), enc_xmin=0.1, enc_ymin=0.1, nw_enc_pcmp=0.1, grw=0.36)
  c.plot()



plus_res_inst
----------------------------------------------------

.. autofunction:: gf180mcu.plus_res_inst

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.plus_res_inst(l_res=0.1, w_res=0.1, res_type='nplus_s', sub=0, cmp_res_ext=0.1, con_enc=0.1, cmp_imp_layer=(32, 0), sub_imp_layer=(31, 0), label=0, r0_label='', r1_label='', sub_label='')
  c.plot()



polyf_res_inst
----------------------------------------------------

.. autofunction:: gf180mcu.polyf_res_inst

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.polyf_res_inst(l_res=0.1, w_res=0.1, res_type='npolyf_s', pl_res_ext=0.1, con_enc=0.1, pl_imp_layer=(32, 0), sub_imp_layer=(31, 0), label=0, r0_label='', r1_label='', sub_label='')
  c.plot()



pplus_res
----------------------------------------------------

.. autofunction:: gf180mcu.pplus_res

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.pplus_res(l_res=0.1, w_res=0.1, res_type='pplus_s', sub=0, deepnwell=0, pcmpgr=0, label=0, r0_label='', r1_label='', sub_label='')
  c.plot()



ppolyf_res
----------------------------------------------------

.. autofunction:: gf180mcu.ppolyf_res

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.ppolyf_res(l_res=0.1, w_res=0.1, res_type='ppolyf_s', deepnwell=0, pcmpgr=0, label=0, r0_label='', r1_label='', sub_label='')
  c.plot()



ppolyf_u_high_Rs_res
----------------------------------------------------

.. autofunction:: gf180mcu.ppolyf_u_high_Rs_res

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.ppolyf_u_high_Rs_res(l_res=0.42, w_res=0.42, volt='3.3V', deepnwell=0, pcmpgr=0, label=0, r0_label='', r1_label='', sub_label='')
  c.plot()



res
----------------------------------------------------

.. autofunction:: gf180mcu.res

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.res(l_res=0.1, w_res=0.1, res_type='rm1', label=0, r0_label='', r1_label='')
  c.plot()



sc_diode
----------------------------------------------------

.. autofunction:: gf180mcu.sc_diode

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.sc_diode(la=0.1, wa=0.1, cw=0.1, m=1, pcmpgr=0, label=0, p_label='', n_label='')
  c.plot()



via_generator
----------------------------------------------------

.. autofunction:: gf180mcu.via_generator

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.via_generator(x_range=(0, 1), y_range=(0, 1), via_size=(0.17, 0.17), via_layer=(66, 44), via_enclosure=(0.06, 0.06), via_spacing=(0.17, 0.17))
  c.plot()



via_stack
----------------------------------------------------

.. autofunction:: gf180mcu.via_stack

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.via_stack(x_range=(0, 1), y_range=(0, 1), base_layer=(22, 0), slotted_licon=0, metal_level=1, li_enc_dir='V')
  c.plot()



well_res
----------------------------------------------------

.. autofunction:: gf180mcu.well_res

.. plot::
  :include-source:

  import gf180

  c = gf180mcu.well_res(l_res=0.42, w_res=0.42, res_type='nwell', pcmpgr=0, label=0, r0_label='', r1_label='', sub_label='')
  c.plot()
