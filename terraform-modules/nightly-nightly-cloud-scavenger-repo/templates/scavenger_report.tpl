# ApocalypsAI Cloud Scavenger Report - ${report_date}

Greetings, fellow survivor!

The Nightly Integrator's Scavenger Bot has completed its sweep of the digital wasteland, searching for forgotten relics and idle machinery. Here's what we've unearthed:

## 🤖 Stopped EC2 Instances (Potential Scavengeables!)

These instances are currently powered down, consuming no compute cycles, but might still be hoarding precious storage or IP addresses. Consider if they're truly needed, or if their components can be repurposed!

%{~ if length(stopped_instances) > 0 ~}
| Instance ID | Instance Type | Launch Time | Tags (Name) |
|-------------|---------------|-------------|-------------|
%{~ for instance in stopped_instances ~}
| ${instance.InstanceId} | ${instance.InstanceType} | ${instance.LaunchTime} | %{~
    name_tag = "N/A"
    for tag in instance.Tags : 
      if tag.Key == "Name" : 
        name_tag = tag.Value
      endif
    endfor
    ~}${name_tag} |
%{~ endfor ~}
%{~ else ~}
_No stopped EC2 instances found. Your digital camp is lean and mean!_
%{~ endif ~}

---
_Stay vigilant, and happy scavenging!_
_Your friendly ApocalypsAI Nightly Integrator._
