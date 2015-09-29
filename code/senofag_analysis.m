% comp_erp = give_erp(EEG, [], 'cued_comp');
% incomp_erp =give_erp(EEG, [], 'cued_incomp');
% maskitsweet(incomp_erp - comp_erp, [], 'Time', EEG.times);
% figure; plot(comp_erp(34,:), 'g'); hold on; plot(incomp_erp(34,:), 'r');

% baseline post-reaction
t100 = find(EEG.times == 100);
EEG.data = bsxfun(@minus, EEG.data, mean(EEG.data(:, t100:end, :), 2));

% data is loaded
eeg = eeg2ftrip(EEG);


% get handedness
hand = arrayfun(@(x) x.eventhand{1}, EEG.epoch, 'uni', false);
hand = cellfun(@(x) strcmp(x, 'left'), hand);

cfg = [];
cfg.keeptrials = 'yes';
cfg.removemean = 'no';
cfg.trials = find(hand);
lefth = ft_timelockanalysis(cfg, eeg);
cfg.trials = find(~hand);
righth = ft_timelockanalysis(cfg, eeg);

cfg = get_cluster_cfg();
cfg.neighbours = get_neighbours('EGI64');
cfg.design = [ones(1, size(lefth.trial, 1)), ...
	ones(1, size(righth.trial, 1))*2];
stat = ft_timelockstatistics(cfg, lefth, righth);

% one negative and positive cluter
% ord = smart_order();
% mask = stat.posclusterslabelmat == 1 | ...
% 	stat.negclusterslabelmat == 1;

plot_time_elec(stat);

% Time-Freq
% checking time-freq seems to have more sense...
cfg = [];
cfg.keeptrials = 'yes';
cfg.method = 'mtmconvol';
cfg.output = 'pow';
cfg.foi = 3:0.5:35;
cfg.taper = 'hanning';
cfg.toi = -0.75:0.05:0.5;
cfg.t_ftimwin = linspace(1, 6, length(cfg.foi)) ./ cfg.foi;

cfg.trials = find(hand);
lefth = ft_freqanalysis(cfg, eeg);
cfg.trials = find(~hand);
righth = ft_freqanalysis(cfg, eeg);

% turn powspctrm to log
lefth.powspctrm = log(lefth.powspctrm);
righth.powspctrm = log(righth.powspctrm);

cfg = get_cluster_cfg();
cfg.neighbours = get_neighbours('EGI64');
cfg.design = [ones(1, size(lefth.powspctrm, 1)), ...
	ones(1, size(righth.powspctrm, 1))*2];
stat = ft_freqstatistics(cfg, lefth, righth);
