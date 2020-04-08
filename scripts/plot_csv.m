%%%%%%%%%%%
% plot_csv.m
%
% Description: Reads CSV filename from console and plots data on a graph.
%              This is a super simple script that assumes 1D data. The
%              intent was to visualize output from our Arduino DAQ
% Author:      Ryan Printup

filename = input("Enter the csv filename: ", 's');
contents = csvread(filename);
plot(contents);

%%% End of File %%%
