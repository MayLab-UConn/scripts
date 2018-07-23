

def renumber_itp_field(in_file, out_file, index_map, columns):
    '''
        Author: Kevin Boyd

        Utility for renumbering fields in an itp. For instance, when making a small change to a molecule such as
        removing a hydrogen, you can throw off the numbering of some of the atoms. This change can propagate to
        thousands of itp line changes, eg in the angle and dihedral terms.

        What this script does is modifies text relating to a single itp field (ie bonds OR angles OR ...). Isolate that
        field so that the numbering starts on the first line (ie, put the field in its own file and take out the [bonds]
        directory -this script can be updated later to ignore these lines, but it can't deal with them for now). A
        dictionary map of old indices : new indices is needed to tell the function which lines to change. If an atom
        is deleted, put a 0 (this is necessary).

        The other thing needed is a list of the columns we're going to operate on. Ie, for bonds, you want to change
        columns 0 and 1, but not 2 (which is the functional form associated with the bond). All columns after the ones
        you want to change will be kept intact, including any comments

        Parameters
            in_file - string path to file
            out_file - string path to output file to make
            index map - dictionary of old_index to new_index, new_index=0 is for deletions
            columns - list of columns to modify, starting from 0  - eg (0, 1, 2) for angles

        TODO
            -allow [ bonds ] and other directives at top of file
            -ignore lines that are comments (start with ";")
            -Allow insertions (right now only supports deletions)
            -add some error messages for cases that shouldn't happen
            -keep string formatting on non-modified columns
    '''
    with open(in_file, 'r') as f_in, open(out_file, 'wt') as f_out:
        for line in f_in:
            writeout = True   # keep track of whether or not line should be written
            splitline = line.strip().split()
            indices_to_replace = [ int(splitline[i]) for i in columns ]  # isolate numbers to replace
            for index, col in zip(indices_to_replace, columns):
                if index_map[index] is not 0:
                    splitline[col] = str(index_map[index])
                else:
                    writeout = False
            if writeout:   # should be true if none of the numbers were 0
                for col in columns:
                    f_out.write("{:>3s}".format(splitline[col]))
                f_out.write(" {:s}\n".format(" ".join(splitline[columns[-1] + 1:])))
