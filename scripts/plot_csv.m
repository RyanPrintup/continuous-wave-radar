filename = input("Enter the csv filename: ", 's');
contents = csvread(filename);
n = 10; % average every n values
a = contents;
b = arrayfun(@(i) mean(a(i:i+n-1)),1:n:length(a)-n+1)'; % the averaged vector

plot(b);
