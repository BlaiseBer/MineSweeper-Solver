from repolib import true_values


class Ordlist:

    def __init__(self, N, liste=None):
        if liste is None:
            liste = []
        liste.sort()
        self.list = liste
        self.N = N


    def add(self, pos):
        k=0
        while k < len(self.list):
            if self.isLess(pos, self.list[k]):
                break
            k+=1
        self.list.insert(k, pos)

    def len(self):
        return len(self.list)

    def isInside(self, pos):
        min = 0
        max = len(self.list)-1
        while (max-min >= 0):
            mid = (max-min)//2 + min
            midv = self.list[mid]
            if midv==pos:
                return True
            elif self.isLess(pos, midv):
                max = mid-1
            else:
                min = mid+1
        return False

    def remove(self, pos):
        min = 0
        max = len(self.list)-1
        while (max - min >= 0):
            mid = (max + min) // 2
            midv = self.list[mid]
            if midv == pos:
                self.list.pop(mid)
                break
            elif self.isLess(pos, midv):
                max = mid-1
            else:
                min = mid+1

    def intersect(self, other):
        L1 = self.list
        L2 = other.list
        L1_inter_L2 = []
        L1_exclude_L2 = []
        L2_exclude_L1 = []

        i1=0
        i2=0
        while (i1<len(L1)) and (i2<len(L2)):
            if L1[i1]==L2[i2]:
                L1_inter_L2.append(L1[i1])
                i1+=1
                i2+=1
            elif self.isLess(L2[i2], L1[i1]):
                L2_exclude_L1.append(L2[i2])
                i2+=1
            else:
                L1_exclude_L2.append(L1[i1])
                i1+=1

        while (i1<len(L1)):
            L1_exclude_L2.append(L1[i1])
            i1+=1

        while (i2<len(L2)):
            L2_exclude_L1.append(L2[i2])
            i2+=1

        return L1_exclude_L2, L1_inter_L2, L2_exclude_L1

    def isLess(self,a,b):
        #return a[0]+a[1]*self.N < b[0]+b[1]*self.N
        return a < b

    def toString(self):
        return str(self.list)
