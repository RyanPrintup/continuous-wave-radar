%%%%%%%%%%%
% averaging_filter_test.m
%
% Description: This script tests an average filter on a csv file containing
%              data points sampled from our Arduino DAQ. 
% Author:      Ryan Printup


% Settings
%
% This is the sample batch sizes to test
batch_sizes = [1, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50];


% Grab file contents
filename = input("Enter the csv filename: ", 's');
contents = csvread(filename);

% Main loop
for batch_i = 1:length(batch_sizes)
    n = batch_sizes(batch_i);   % The batch size
    data_out = [];              % The averaged data
    data_i = 1;                 % The averaged data index
    
    % Loop over content array by batch size
    for i = 1:n:length(contents)
        batch_end = i + n - 1;  % Ending index of the batcj
        
        % Make sure batch doesn't exceed array length
        if (batch_end < length(contents))
            % Compute batch average, store in data_out, and increment index
            data_out(data_i) = mean(contents(i:(i + n - 1)));
            data_i = data_i + 1;
        end
    end
    
    % Plot averaged data to its own plot
    figure(batch_i);
    plot(data_out);
end

%%% End of File %%%
