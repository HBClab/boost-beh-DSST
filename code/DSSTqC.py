
<<<<<<< HEAD
=======
# run Quality Check against new sub data
>>>>>>> d2216bd41e297886bb5f25ee37a8623efde8bebc

import os
import sys
import pandas as pd
from math import pi

def parse_cmd_args():
    import argparse
    parser = argparse.ArgumentParser(description='QC for ATS')
    parser.add_argument('-s', type=str, help='Path to submission')
    parser.add_argument('-o', type=str, help='Path to output for QC plots and Logs')
    parser.add_argument('-sub', type=str, help='Subject ID')

    return parser.parse_args()

def df(submission):
    pd.read_csv(submission)
    return submission

def qc(submission):
    # convert submission to DataFrame
    submission = pd.read_csv(submission)
     # check if submission is a DataFrame
    if not isinstance(submission, pd.DataFrame):
        raise ValueError('Submission is not a DataFrame. Could not run QC')
    # check if submission is empty
    if submission.empty:
        raise ValueError('Submission is empty')
    # check if submission has correct columns 
    if not all(col in submission.columns for col in ['Symbol', 'acc_sum', 'block_c', 'block_dur', 'clicked_response', 'condition', 'continue_roi_ticked', 'correct', 'correct_response', 'countdown', 'cursor_x', 'cursor_y', 'datetime', 'endtime', 'my_cursor_roi', 'my_cursor_roi_ticked', 'project', 'response', 'session_number', 'start_end', 'starttime', 'subject_id', 'task', 'task_vers', 'time_test_box_response', 'time_test_clicked_response', 'time_test_display_stimuli', 'trial', 'x_continue_box', 'y_continue_box']):
        raise ValueError('Submission is missing columns')
    # check if submission has correct number of rows (within 5% of expected = 180)

    
def plots(submission, output, sub):
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns


    df = pd.read_csv(submission)
    #subtract is number of rows that are not test
    df = df[df['condition'] == 'test']


    total = (df['acc_sum'].max() + 1)


    total_correct = df['correct'].sum()

    
    
    percent_correct = total_correct/total
   

    def plot_circular_bar_graph(percentages, name, output_name):
            startangle = 90
            colors = ['#4393E5', '#43BAE5', '#7AE6EA', '#E5A443']
            
            # Convert data to fit the polar axis
            ys = [i *1.1 for i in range(len(percentages))]   # One bar for each block
            left = (startangle * pi * 2) / 360  # This is to control where the bar starts

            # Figure and polar axis
            fig, ax = plt.subplots(figsize=(6, 6))
            ax = plt.subplot(projection='polar')

            # Plot bars and points at the end to make them round
            for i, (block, percentage) in enumerate(percentages.items()):
                ax.barh(ys[i], percentage * 2 * pi, left=left, height=0.5, color=colors[i % len(colors)], label=block)
                ax.text(percentage + left + 0.02, ys[i], f'{percentage:.0%}', va='center', ha='left', color='black', fontsize=12)

            plt.ylim(-1, len(percentages))

            # Custom legend
            ax.legend(loc='center', frameon=True) 

            # Clear ticks and spines
            plt.xticks([])
            plt.yticks([])
            ax.spines.clear()
            plt.title(name, fontsize=15, pad=20, color="white")

            plt.savefig(os.path.join(output, f'{sub}_'+output_name+'.png'))
            plt.close()
    
    plot_circular_bar_graph({'Correct': percent_correct}, 'Accuracy', 'DSST_acc_{sub}')
    avg_time = []
    for i in range(len(df)):
        if i == 0:
            avg_time.append(120000 - df['countdown'][i+10])
        else:
            avg_time.append(df['countdown'][i+9] - df['countdown'][i+10])
 
    #create a scatterplot of reaction time with transparent box and whisker. Use transparent dots to show density and demarcate by correct or incorrect
    new_df = pd.DataFrame({'reaction_time': avg_time, 'correct': df['correct']})
    new_df['TEST BLOCK'] = 'TEST BLOCK'  # Add a constant column for the x-axis

    plt.figure(figsize=(10, 6))
    sns.boxplot(x='TEST BLOCK', y='reaction_time', data=new_df, showfliers=False)
    sns.stripplot(x='TEST BLOCK', y='reaction_time', data=new_df, jitter=True, alpha=0.5, hue='correct')
    plt.xlabel('')  # Remove the x-axis label
    plt.ylabel('Reaction Time (ms)')
    plt.title('Reaction Time by Correct or Incorrect')
    plt.savefig(os.path.join(output, f'{sub}_DSST_rt.png'))
    

def main():

    #parse command line arguments
    args = parse_cmd_args()
    submission = args.s
    output = args.o
    sub = args.sub

    # check if submission is a csv
    if not submission.endswith('.csv'):
        raise ValueError('Submission is not a csv')
    # check if submission exists
    if not os.path.exists(submission):
        raise ValueError('Submission does not exist')
    # run QC
    qc(submission)
    
    print(f'QC passed for {submission}, generating plots...')
    # generate plots
    plots(submission, output, sub)
    return submission
    
    
if __name__ == '__main__':
<<<<<<< HEAD
    main()
=======
    main()
>>>>>>> d2216bd41e297886bb5f25ee37a8623efde8bebc
