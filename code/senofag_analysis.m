% comp_erp = give_erp(EEG, [], 'cued_comp');
% incomp_erp =give_erp(EEG, [], 'cued_incomp');
% maskitsweet(incomp_erp - comp_erp, [], 'Time', EEG.times);
% figure; plot(comp_erp(34,:), 'g'); hold on; plot(incomp_erp(34,:), 'r');

% data is loaded
eeg = eeg2ftrip(EEG);

cfg = [];
cfg.keeptrials = 'yes';
cfg.trials = find(epoch_centering_events(EEG, 'cued_incomp'));
incomp = ft_timelockanalysis(cfg, eeg);
cfg.trials = find(epoch_centering_events(EEG, 'cued_comp'));
comp = ft_timelockanalysis(cfg, eeg);

cfg = get_cluster_cfg();
cfg.neighbours = get_neighbours('EGI64');
cfg.design = [ones(1, size(comp.trial, 1)), ...
	ones(1, size(incomp.trial, 1))*2];
stat = ft_timelockstatistics(cfg, comp, incomp);

% one negative and positive cluter
% ord = smart_order();
% mask = stat.posclusterslabelmat == 1 | ...
% 	stat.negclusterslabelmat == 1;

plot_time_elec(stat);
e = explore_stuff(EEG, stat.stat, {'comp > incomp'});


% check component 1:
comp = 3;
comp_erp = give_erp(EEG, comp, 'cued_comp', 'ica');
incomp_erp = give_erp(EEG, comp, 'cued_incomp', 'ica');
figure; plot(comp_erp, 'g'); hold on; plot(incomp_erp, 'r');