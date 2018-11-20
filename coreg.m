function coreg(ref, moving)
    refI = spm_vol(ref);
    refM = spm_vol(moving);
    x=spm_coreg(refI, refM, struct('cost_fun','mi'));
    M = spm_matrix(x);
    spm_get_space(moving, M * refM.mat)
    spm_reslice({ref;moving}, struct('interp',0,'which',1,'prefix','','mean',false))
end