% setify sketch
chanloc = 'E:\\olga K\\N170\\n170_artykuł\\CODE_eeg_beh\\braintools-master\\chan\\loc\\GSN-HydroCel-65 1.0.sfp'
EEG = pop_readegi('E:\proj\senofag\data\RAW\MD_03_4_20150924_053115.raw', [],[],'auto');
EEG=pop_chanedit(EEG, 'load', ...
	{chanloc, 'filetype', 'autodetect'}, ...
	'changefield', {68, 'datachan', 0}, ...
	'setref',{'1:67' 'Cz'});
[ALLEEG EEG] = eeg_store(ALLEEG, EEG, CURRENTSET);

EEG = pop_eegfiltnew(EEG, [], 1, 826, true, [], 0);
EEG = pop_reref( EEG, [], 'refloc', ...
	struct('labels', {'Cz'}, ...
	'Y', {0}, 'X', {6.2205e-16}, 'Z', {10.1588}, 'sph_theta', {0}, ...
	'sph_phi', {90}, 'sph_radius', {10.1588}, 'theta', {0}, ...
	'radius', {0}, 'type', {''}, 'ref', {''}, 'urchan', {68}, ...
	'datachan',{0}), ...
	'exclude',[17 39 59] );
[ALLEEG EEG CURRENTSET] = pop_newset(ALLEEG, EEG, 2,'gui','off');

% how to get effect events:
evnt = {EEG.event.type};
dins = arrayfun(@(x) ['DI', num2str(x)], 10:17, 'uni', false);
test = cellfun(@(x) find(strcmp(x, evnt)), dins, 'uni', false);
test = [test{:}];