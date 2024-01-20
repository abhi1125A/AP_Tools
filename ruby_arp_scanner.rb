#!/usr/bin/ruby
require 'socket'

if ARGV.length != 1
  puts "Usage: #{$0} <subnet>"
  puts "Example: #{$0} 192.168.1"
  exit(1)
end

subnet = ARGV[0]

s = UDPSocket.new

254.times do |i|
  next if i == 0
  s.send("test", 0, "#{subnet}.#{i}", 53)
end

f = File.open("/proc/net/arp", 'r')
data = f.read.split("\n")
up_hosts = []

data.each do |line|
  entry = line.split(/\s+/)
  next if entry[3] == "00:00:00:00:00:00"
  next if entry[0] == "IP"
  up_hosts << { ip: entry[0], mac: entry[3] }
end

puts "Active Network Hosts"
puts "%-12s\t%s" % [" IP Addr", "Mac Addresses"]

up_hosts.each do |host|
  puts "%-12s\t%s" % [host[:ip], host[:mac]]
end
