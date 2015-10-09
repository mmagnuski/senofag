% setify sketch

rawdir = 'C:\Users\Ola\Dropbox\Sarenka\senofag eeg\RAW';
dtdir = 'E:\Programy\EXP\senofag\data';
file = 'senofag_02_MC_20150917_044204_1.raw';
fpath = fullfile(rawdir, file);

bt = fileparts(which('braintools'));
chanloc = fullfile(bt, '\chan\loc\GSN-HydroCel-65 1.0.sfp');

EEG = pop_readegi(fpath, [],[],'auto');
EEG=pop_chanedit(EEG, 'load', ...
	{chanloc, 'filetype', 'autodetect'}, ...
	'changefield', {68, 'datachan', 0}, ...
	'setref',{'1:67' 'Cz'});

EEG = pop_eegfiltnew(EEG, [], 1, 826, true, [], 0);
Cz_ind = find(strcmp('Cz', {EEG.chaninfo.nodatchans.labels}));
Cz_loc = EEG.chaninfo.nodatchans(Cz_ind);
Cz_loc.type = '';
Cz_loc.urchan = 68;

EEG = pop_reref( EEG, [], 'refloc', ...
	Cz_loc, 'exclude', [17, 54]);

% EEG = pop_reref( EEG, [], 'refloc', ...
% 	Cz_loc, 'exclude',[17 39 59]);

wtimes = csvread(fullfile(dtdir, 's2_wtimes.csv'));
EEG = senofag_senofag_recode_marks(EEG, wtimes);

% how to get effect events:
evnt = {EEG.event.type};
dins = arrayfun(@(x) ['DI', num2str(x)], 10:17, 'uni', false);
test = cellfun(@(x) find(strcmp(x, evnt)), dins, 'uni', false);
test = [test{:}];