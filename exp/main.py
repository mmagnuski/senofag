import os
from settings import create_settings, create_block, get_colors_from_square
from stim import subject_id_gui, create_stimuli, run_block, Instructions


subject_id = subject_id_gui()
settings = create_settings(short_test=False, send_triggers=False)
settings['subject name'] = subject_id
stim = create_stimuli(fullscr=True, settings=settings)
trigger = stim['trigger']
# colors = st.shuffle_colors(stim)

# make sure data dir exists
if not os.path.isdir(settings['data dir']):
    os.mkdir(settings['data dir'])

# show instructions
show_instructions = True
instr_dir = os.path.join(os.getcwd(), 'instr')
instructions = [os.path.join(instr_dir, f) for f in os.listdir(instr_dir)]
if len(instructions) > 0:
	instr = Instructions(stim['win'], instructions)
	instr.present(stop=11)

# TODO - add training block(s)

colors = ['red', 'green', 'yellow', 'blue']
for block_number in range(4):
    block_df = create_block(block_number, settings=settings)
    cond_color = get_colors_from_square(colors, block_number, settings=settings)
    run_block(block_df, stim, block_num=block_number, effect_colors=cond_color,
              trigger=trigger, settings=settings)
    # TODO - show between-block instructions
