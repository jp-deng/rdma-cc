import argparse
import sys
import os
import nutils

config_template="""ENABLE_QCN 1
USE_DYNAMIC_PFC_THRESHOLD 1

PACKET_PAYLOAD_SIZE 1000

TOPOLOGY_FILE ../topology_gen/{topo}.txt
FLOW_FILE ../traffic_gen/{trace}.txt
TRACE_FILE mix/trace.txt
FCT_OUTPUT_FILE mix/fct_{output_file}.txt
PFC_OUTPUT_FILE mix/pfc_{output_file}.txt

SIMULATOR_STOP_TIME 4.00

CC_MODE {mode}
MP_MODE {mp_mode}
ALPHA_RESUME_INTERVAL {t_alpha}
RATE_DECREASE_INTERVAL {t_dec}
CLAMP_TARGET_RATE 0 
RP_TIMER {t_inc}
EWMA_GAIN {g}
FAST_RECOVERY_TIMES 1
RATE_AI {ai}Mb/s
RATE_HAI {hai}Mb/s
MIN_RATE 1000Mb/s
DCTCP_RATE_AI {dctcp_ai}Mb/s

ERROR_RATE_PER_LINK 0.0000
L2_CHUNK_SIZE 4000
L2_ACK_INTERVAL 1
L2_BACK_TO_ZERO 0

HAS_WIN {has_win}
GLOBAL_T 1
VAR_WIN {vwin}
FAST_REACT {us}
U_TARGET {u_tgt}
MI_THRESH {mi}
INT_MULTI {int_multi}
MULTI_RATE 0
SAMPLE_FEEDBACK 0
PINT_LOG_BASE {pint_log_base}
PINT_PROB {pint_prob}

RATE_BOUND 1

ACK_HIGH_PRIO {ack_prio}

LINK_DOWN {link_down}

ENABLE_TRACE {enable_tr}

KMAX_MAP {kmax_map}
KMIN_MAP {kmin_map}
PMAX_MAP {pmax_map}
BUFFER_SIZE {buffer_size}
QLEN_MON_FILE mix/qlen_{topo}_{trace}_{cc}{failure}.txt
QLEN_MON_START 2000000000
QLEN_MON_END 3000000000
"""


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='run simulation')
	parser.add_argument('--cc', dest='cc', action='store', default='dcqcn', help="congestion control")
	parser.add_argument('--mp', dest='mp', action='store', default='none', help="multi path")
	parser.add_argument('--trace', dest='trace', action='store', default='oeswitch', help="the name of the flow file")
	parser.add_argument('--bw', dest="bw", action='store', default='10', help="the NIC bandwidth")
	parser.add_argument('--down', dest='down', action='store', default='0 0 0', help="link down event")
	parser.add_argument('--topo', dest='topo', action='store', default='spine_leaf', help="the name of the topology file")
	parser.add_argument('--utgt', dest='utgt', action='store', type=int, default=95, help="eta of HPCC")
	parser.add_argument('--mi', dest='mi', action='store', type=int, default=0, help="MI_THRESH")
	parser.add_argument('--hpai', dest='hpai', action='store', type=int, default=0, help="AI for HPCC")
	parser.add_argument('--pint_log_base', dest='pint_log_base', action = 'store', type=float, default=1.01, help="PINT's log_base")
	parser.add_argument('--pint_prob', dest='pint_prob', action = 'store', type=float, default=1.0, help="PINT's sampling probability")
	parser.add_argument('--enable_tr', dest='enable_tr', action = 'store', type=int, default=0, help="enable packet-level events dump")
	args = parser.parse_args()

	topo=args.topo
	bw = int(args.bw)
	trace = args.trace
	#bfsz = 16 if bw==50 else 32
	bfsz = 16 * bw * 4 / 50
	u_tgt=args.utgt/100.
	mi=args.mi
	pint_log_base=args.pint_log_base
	pint_prob = args.pint_prob
	enable_tr = args.enable_tr
	load = ''
	traffic = ''

	parts = args.trace.split('_')
	if len(parts) >= 2:
		traffic = parts[0]
		load = parts[1]

	failure = ''
	if args.down != '0 0 0':
		failure = '_down'

	kmax_map = "3 %d %d %d %d %d %d"%(bw*1000000000, 400*bw/25, bw*4*1000000000, 400*bw*4/25, bw*10*1000000000, 400*bw*10/25)
	kmin_map = "3 %d %d %d %d %d %d"%(bw*1000000000, 100*bw/25, bw*4*1000000000, 100*bw*4/25, bw*10*1000000000, 100*bw*10/25)
	pmax_map = "3 %d %.2f %d %.2f %d %.2f"%(bw*1000000000, 0.2, bw*4*1000000000, 0.2, bw*10*1000000000, 0.2)

	# if trace == "multismallflow" or trace == "multismallflow":
	# 	if args.cc == "hp":
	# 		args.cc = "hpccPint"
	# if trace == "oeswitch":
	# 	topo = "spine_leaf_test"
	# 	if args.cc == "newcc":
	# 		args.cc = "hpccPint"

	mp_mode = 0
	output_file = "%s_%s_%s"%(topo, trace, args.cc)
	if args.mp == "newmp":
		mp_mode = 1
		output_file = "%s_%s_%s"%(topo, trace, args.mp)
	elif args.mp == "mprdma":
		output_file = "%s_%s_%s"%(topo, trace, args.mp)
	elif args.mp == "conweave":
		output_file = "%s_%s_%s"%(topo, trace, args.mp)

	config_name = "mix/config_%s.txt"%(output_file)

	if (args.cc.startswith("dcqcn")):
		ai = 5 * bw / 25
		hai = 50 * bw /25

		if args.cc == "dcqcn":
			config = config_template.format(trace=trace, topo=topo, cc=args.cc, output_file=output_file, mode=1, mp_mode = mp_mode, t_alpha=1, t_dec=4, t_inc=300, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=0, vwin=0, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, pint_log_base=pint_log_base, pint_prob=pint_prob, ack_prio=1, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz, enable_tr=enable_tr)
		elif args.cc == "dcqcn_paper":
			config = config_template.format(trace=trace, topo=topo, cc=args.cc, output_file=output_file, mode=1, mp_mode = mp_mode, t_alpha=50, t_dec=50, t_inc=55, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=0, vwin=0, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, pint_log_base=pint_log_base, pint_prob=pint_prob, ack_prio=1, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz, enable_tr=enable_tr)
		elif args.cc == "dcqcn_vwin":
			config = config_template.format(trace=trace, topo=topo, cc=args.cc, output_file=output_file, mode=1, mp_mode = mp_mode, t_alpha=1, t_dec=4, t_inc=300, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=1, vwin=1, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, pint_log_base=pint_log_base, pint_prob=pint_prob, ack_prio=0, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz, enable_tr=enable_tr)
		elif args.cc == "dcqcn_paper_vwin":
			config = config_template.format(trace=trace, topo=topo, cc=args.cc, output_file=output_file, mode=1, mp_mode = mp_mode, t_alpha=50, t_dec=50, t_inc=55, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=1, vwin=1, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, pint_log_base=pint_log_base, pint_prob=pint_prob, ack_prio=0, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz, enable_tr=enable_tr)
	elif args.cc == "hp":
		ai = 10 * bw / 25;
		if args.hpai > 0:
			ai = args.hpai
		hai = ai # useless
		int_multi = bw / 25;
		if int_multi == 0:
			int_multi = 1
		cc = "%s%d"%(args.cc, args.utgt)
		if (mi > 0):
			cc += "mi%d"%mi
		if args.hpai > 0:
			cc += "ai%d"%ai
		config = config_template.format(trace=trace, topo=topo, cc=cc, output_file=output_file, mode=3, mp_mode = mp_mode, t_alpha=1, t_dec=4, t_inc=300, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=1, vwin=1, us=1, u_tgt=u_tgt, mi=mi, int_multi=int_multi, pint_log_base=pint_log_base, pint_prob=pint_prob, ack_prio=0, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz, enable_tr=enable_tr)
	elif args.cc == "dctcp":
		ai = 10 # ai is useless for dctcp
		hai = ai  # also useless
		dctcp_ai=615 # calculated from RTT=13us and MTU=1KB, because DCTCP add 1 MTU per RTT.
		kmax_map = "3 %d %d %d %d %d %d"%(bw*1000000000, 30*bw/10, bw*4*1000000000, 30*bw*4/10, bw*10*1000000000, 30*bw*10/10)
		kmin_map = "3 %d %d %d %d %d %d"%(bw*1000000000, 30*bw/10, bw*4*1000000000, 30*bw*4/10, bw*10*1000000000, 30*bw*10/10)
		pmax_map = "3 %d %.2f %d %.2f %d %.2f"%(bw*1000000000, 1.0, bw*4*1000000000, 1.0, bw*10*1000000000, 1.0)
		config = config_template.format(trace=trace, topo=topo, cc=args.cc, output_file=output_file, mode=8, mp_mode = mp_mode, t_alpha=1, t_dec=4, t_inc=300, g=0.0625, ai=ai, hai=hai, dctcp_ai=dctcp_ai, has_win=1, vwin=1, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, pint_log_base=pint_log_base, pint_prob=pint_prob, ack_prio=0, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz, enable_tr=enable_tr)
	elif args.cc == "timely":
		ai = 10 * bw / 10
		hai = 50 * bw / 10
		config = config_template.format(trace=trace, topo=topo, cc=args.cc, output_file=output_file, mode=7, mp_mode = mp_mode, t_alpha=1, t_dec=4, t_inc=300, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=0, vwin=0, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, pint_log_base=pint_log_base, pint_prob=pint_prob, ack_prio=1, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz, enable_tr=enable_tr)
	elif args.cc == "timely_vwin":
		ai = 10 * bw / 10;
		hai = 50 * bw / 10;
		config = config_template.format(trace=trace, topo=topo, cc=args.cc, output_file=output_file, mode=7, mp_mode = mp_mode, t_alpha=1, t_dec=4, t_inc=300, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=1, vwin=1, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, pint_log_base=pint_log_base, pint_prob=pint_prob, ack_prio=1, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz, enable_tr=enable_tr)
	elif args.cc == "hpccPint":
		ai = 10 * bw / 25;
		if args.hpai > 0:
			ai = args.hpai
		hai = ai # useless
		int_multi = bw / 25;
		cc = "%s%d"%(args.cc, args.utgt)
		if (mi > 0):
			cc += "mi%d"%mi
		if args.hpai > 0:
			cc += "ai%d"%ai
		cc += "log%.3f"%pint_log_base
		cc += "p%.3f"%pint_prob
		config = config_template.format(trace=trace, topo=topo, cc=cc, output_file=output_file, mode=10, mp_mode = mp_mode, t_alpha=1, t_dec=4, t_inc=300, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=1, vwin=1, us=1, u_tgt=u_tgt, mi=mi, int_multi=int_multi, pint_log_base=pint_log_base, pint_prob=pint_prob, ack_prio=0, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz, enable_tr=enable_tr)
	elif args.cc == "newcc":
		ai = 10 * bw / 10
		hai = 50 * bw / 10
		config = config_template.format(trace=trace, topo=topo, cc=args.cc, output_file=output_file, mode=6, mp_mode = mp_mode, t_alpha=1, t_dec=4, t_inc=300, g=0.00390625, ai=ai, hai=hai, dctcp_ai=1000, has_win=1, vwin=1, us=0, u_tgt=u_tgt, mi=mi, int_multi=1, pint_log_base=pint_log_base, pint_prob=pint_prob, ack_prio=1, link_down=args.down, failure=failure, kmax_map=kmax_map, kmin_map=kmin_map, pmax_map=pmax_map, buffer_size=bfsz, enable_tr=enable_tr)
	else:
		print "unknown cc:", args.cc
		sys.exit(1)

	with open(config_name, "w") as file:
		file.write(config)
	
	ret = 1
	if args.mp == "mprdma":
		ret = os.system("sudo ./waf --run 'scratch/mp-rdma-simulator %s'"%(config_name))
		# os.system("sudo ./waf --run scratch/mp-rdma-simulator --command-template=\"gdb --args %%s %s \" "%(config_name))
	else:
		# os.system("sudo ./waf --run scratch/rdma-simulator --command-template=\"gdb --args %%s %s \" "%(config_name))
		ret = os.system("sudo ./waf --run 'scratch/rdma-simulator %s'"%(config_name))
	
	# if ret == 0:
	nutils.process(args.mp, traffic, args.cc, load)		



