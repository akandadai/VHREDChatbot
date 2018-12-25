from processing import load_word_vectors, string_to_vec #, train_prep_default, index_to_word
from VRED import * #build_model (remove *)



if __name__ == '__main__':
    

    ## add argparse later
    
    #set hparams
    
    #model = build_model
    
    if mode == 'train':
        #format data and save as csv? OR assume
        #(x_enc, x_dec, y_actual) = train_prep_default()
        #model.train(...)
        #model.save(...)
    elif mode == 'chat':
        
        while True:
            phrase = str(input(input_prompt))
            if phrase == end_token:
                print("Exiting.")
                break
            
            #response_ind = model.predict()
            #Strings = " ".join(index_to_word(response_ind)
            print(output_prompt + Strings)
            
