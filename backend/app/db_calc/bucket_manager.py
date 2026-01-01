class BucketManager:
    
  def __init__(self, pos_list):
    self.pos_dict = {}
    for x in pos_list:
        self.pos_dict[x] = []

  def add_player(self, player_name, player_pos, value):
    self.pos_dict[player_pos] += [(player_name, value)]

  def empty_bucket(self, category, quantity):
    self.pos_dict[category].sort(key=lambda tup: tup[1], reverse=True)  # sorts in place

    to_remove = []
    for name,_ in self.pos_dict[category][:quantity]:
      for k in self.pos_dict.keys():
        for t in self.pos_dict[k]:
          # print("t0 v name " + str(t[0]) + " " + str(name))
          if t[0] == name:
            to_remove += [t]
    ret_val = self.pos_dict[category][:quantity]
    for tup in to_remove:
      # print("tup " + str(tup) + " " + str(self.pos_dict[k]))
      for k in self.pos_dict.keys():
        if tup in self.pos_dict[k]:
          self.pos_dict[k].remove(tup)

    return ret_val


  def __str__(self):
    return str(self.pos_dict)


