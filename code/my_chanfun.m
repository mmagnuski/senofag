function my_chanfun(EEG, stat, fig, chan)

persistent comp_erp
persistent incomp_erp

if isempty(comp_erp)
    comp_erp = give_erp(EEG, [], 'cued_comp');
    incomp_erp =give_erp(EEG, [], 'cued_incomp');
end

mask = get_cluster_mask(stat);
ax = findobj('type', 'axes', 'parent', fig);
axes(ax);
cla
plot(EEG.times, comp_erp(chan,:), 'g');
plot(EEG.times, incomp_erp(chan,:), 'r');
legend('comp', 'incomp');
% mark clusters
