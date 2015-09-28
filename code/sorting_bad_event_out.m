% reading relevant files
mtarg = []
i = 0;
f = fopen('s3_mtarg.csv');
line = fgets(f);
while ischar(line)
i = i + 1; mtarg(i) = str2num(line);
line = fgets(f);
end
fclose(f);

wtimes = []
i = 0;
f = fopen('s3_wtimes.txt');
line = fgets(f);
while ischar(line)
i = i + 1; wtimes(i) = str2num(line);
line = fgets(f);
end
fclose(f);

% checking which eeg event is unnecessary
eeg_targ = regexp(evnt, 'DIN[23]', 'match', 'once');
eeg_targ = eeg_targ(~cellfun(@isempty, eeg_targ));
eeg_targ = cellfun(@str2num, regexp(eeg_targ, '[0-9]+', 'match', 'once'));

figure; axes(); hold on; plot(eeg_targ, 'r'); plot(mtarg, 'g');


% to find the bad event in time (plot it and remove)
tev = cellfun(@(x) find(strcmp(evnt, x)), {'DIN2', 'DIN3'}, 'Uni', false);
tev = [tev{:}];
tev = sort(tev);
EEG.event(tev(35))
EEG.event(tev(35)) = [];