import numpy as np
import scipy
import accessify

class Computing:
    def __init__(self, matirx):
        self.__params = matirx
    
    @accessify.private
    def FindMaxInColumnWithExclitedRows(self, column_id, excluded_rows):
        matrix = np.copy(self.__params)
        col = matrix[:, column_id]

        mask = np.ones(len(col), bool)
        excluded_idx = [int(idx) for idx in excluded_rows]
        mask[excluded_idx] = False

        filtered_columns = col[mask]

        max_val = np.max(filtered_columns)

        avel_max = np.where(mask)[0]
        max_filt_id = np.argmax(filtered_columns)
        mat_max_id = avel_max[max_filt_id]

        return max_val, mat_max_id

    @accessify.private
    def FindKMinInColumnWithExclitedRows(self, column_id, excluded_rows, k=1):
        col =  np.asarray(self.__params)[:, column_id]
        n = col.shape[0]

        mask = np.ones(len(col), bool)
        excluded_indices = [int(idx) for idx in excluded_rows]
        mask[excluded_indices] = False

        avail_idx = np.nonzero(mask)[0]
        filtered_columns = col[mask]

        if k == 1:
            min_pos = int(np.argmin(filtered_columns))
            return filtered_columns[min_pos], int(avail_idx[min_pos])

        kth_value = np.partition(filtered_columns, k - 1)[k - 1]
        idx_k_small = np.argpartition(filtered_columns, k - 1)[:k]
        small_values = filtered_columns[idx_k_small]
    
        eq_positions = np.nonzero(small_values == kth_value)[0]
        if eq_positions.size > 0:
            chosen_local = int(idx_k_small[eq_positions[0]])
        else:
            chosen_local = int(idx_k_small[np.argmax(small_values)])

        return kth_value, int(avail_idx[chosen_local])

    def HungarianMinimum(self):
        row_ind, col_ind = scipy.optimize.linear_sum_assignment(self.__params)
        sorted_indices = np.argsort(col_ind)
        row_ind = row_ind[sorted_indices]
        col_ind = col_ind[sorted_indices]
        
        values = self.__params[row_ind, col_ind]
        cost = values.sum()
        return cost, values
    
    def HungarianMaximum(self):
        matrix = -self.__params.copy()
        row_ind, col_ind = scipy.optimize.linear_sum_assignment(matrix)
        sorted_indices = np.argsort(col_ind)
        row_ind = row_ind[sorted_indices]
        col_ind = col_ind[sorted_indices]
        
        values = self.__params[row_ind, col_ind]
        cost = values.sum()
        return cost, values

    def ThriftyMethod(self):
        cost = 0
        shapes = self.__params.shape
        assigned_rows = set()
        values = []

        for i in range(shapes[0]):
            min_val, row = self.FindKMinInColumnWithExclitedRows(i, assigned_rows)
            cost += min_val
            assigned_rows.add(row)
            values.append(min_val)
        
        return cost, np.array(values)
    
    def GreedyMethod(self):
        cost = 0
        shapes = self.__params.shape
        assigned_rows = set()
        values = []

        for i in range(shapes[1]):
            max_val, row = self.FindMaxInColumnWithExclitedRows(i, assigned_rows)
            if row != -1:
                cost += max_val
                assigned_rows.add(row)
                values.append(max_val)

        return cost, np.array(values)
    

    def Greedy_ThreftyMetodX(self, x):
        cost = 0
        shapes = self.__params.shape
        assigned_rows = set()
        values = []

        for i in range(shapes[1]):
            if i < x:
                val, row = self.FindMaxInColumnWithExclitedRows(i, assigned_rows)
                if row != -1:
                    cost += val
                    assigned_rows.add(row)
                    values.append(val)

            else:
                val, row = self.FindKMinInColumnWithExclitedRows(i, assigned_rows)
                if row != -1:
                    cost += val
                    assigned_rows.add(row)
                    values.append(val)

        return cost, np.array(values)
    
    def Threfty_GreedyMetodX(self, x):
        cost = 0
        shapes = self.__params.shape
        assigned_rows = set()
        values = []

        for i in range(shapes[1]):
            if i < x:
                val, row = self.FindKMinInColumnWithExclitedRows(i, assigned_rows)
                if row != -1:
                    cost += val
                    assigned_rows.add(row)
                    values.append(val)

            else:
                val, row = self.FindMaxInColumnWithExclitedRows(i, assigned_rows)
                if row != -1:
                    cost += val
                    assigned_rows.add(row)
                    values.append(val)

        return cost, np.array(values)

    def TkG_MethodX(self, k, x):
        cost = 0
        shapes = self.__params.shape
        assigned_rows = set()
        values = []

        for i in range(shapes[1]):
            if (i < x) and (i + k < shapes[1]):
                val, row = self.FindKMinInColumnWithExclitedRows(i, assigned_rows, k)
                if row != -1:
                    cost += val
                    assigned_rows.add(row)
                    values.append(val)

            else:
                val, row = self.FindMaxInColumnWithExclitedRows(i, assigned_rows)
                if row != -1:
                    cost += val
                    assigned_rows.add(row)
                    values.append(val)
        
        return cost, np.array(values)