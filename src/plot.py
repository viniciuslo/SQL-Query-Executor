import matplotlib.pyplot as plt

def plot_graph(button, result_text, image_widget):
    global query_result
    print("Plotting graph")
    if query_result is not None:
        try:
            query_result.plot(kind='bar', x='name', y='salary')
            plt.savefig('data/query_result_plot.png')
            plt.close()
            image_widget.set_image('data/query_result_plot.png')
            result_text.set_text(result_text.get_text()[0] + "\n\nGraph plotted below:")
        except Exception as e:
            result_text.set_text(result_text.get_text()[0] + f"\n\nError plotting graph: {str(e)}")
    else:
        result_text.set_text('Execute or load a query first.')
