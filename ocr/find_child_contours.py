from numba import jit

@jit(nopython=True)
def find_child_contours(contours, hierarchy, img_cnt_delete):
    for i in range(len(hierarchy[0])):
        count_children = 0
        index_child = 0
        if hierarchy[0][i][2] != -1:
            count_children += 1
            index_child = hierarchy[0][i][2]
            while hierarchy[0][index_child][0] != -1:
                count_children += 1
                index_child = hierarchy[0][index_child][0]
            else:
                pass
        if count_children > 5:
            cnt_delete = contours[i]
            for j in cnt_delete:
                img_cnt_delete[j[0][1], j[0][0]] = 0
        else:
            pass
    return img_cnt_delete